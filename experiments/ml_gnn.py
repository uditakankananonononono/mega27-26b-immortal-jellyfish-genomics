"""GNN species discriminator on k-mer co-occurrence graphs of upstream regions.

Each upstream region -> graph: nodes = distinct canonical 6-mers (capped at 128
most frequent), node features = [norm count, GC frac, mean position frac,
positional spread]; edges = adjacent-occurrence co-occurrence (symmetric
normalized adjacency). Two-layer GCN + mean pool + linear head.
Task: T. dohrnii vs A. aurita upstream discrimination (positives only).
Baseline: 6-mer logistic regression on the same data. 5-fold CV x 5 seeds.
Output: results/ml_gnn.json
"""
import json, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jellyfish.ml import kmer_vector
from jellyfish.motifs import canonical
import torch
from torch import nn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

K = 6
MAXN = 128

def graph_from_seq(seq):
    """Nodes: distinct canonical k-mers (top MAXN by count). Features per node:
    [count_norm, gc, mean_pos, pos_std]. Edges: consecutive k-mer co-occurrence."""
    seq = seq.upper()
    km = []
    for i in range(len(seq) - K + 1):
        w = seq[i:i+K]
        if "N" not in w:
            km.append(canonical(w))
    if len(km) < 10:
        return None
    from collections import Counter
    cnt = Counter(km)
    vocab = [k for k, _ in cnt.most_common(MAXN)]
    vidx = {k: i for i, k in enumerate(vocab)}
    n = len(vocab)
    X = np.zeros((n, 4), dtype=np.float32)
    positions = {k: [] for k in vocab}
    for p, k in enumerate(km):
        if k in vidx:
            positions[k].append(p / len(km))
    for k, i in vidx.items():
        ps = positions[k]
        X[i] = [cnt[k] / len(km), (k.count("G") + k.count("C")) / K,
                float(np.mean(ps)), float(np.std(ps)) if len(ps) > 1 else 0.0]
    A = np.zeros((n, n), dtype=np.float32)
    for a, b in zip(km, km[1:]):
        if a in vidx and b in vidx:
            A[vidx[a], vidx[b]] += 1
            A[vidx[b], vidx[a]] += 1
    D = np.diag(1.0 / np.sqrt(A.sum(1) + 1e-9))
    Anorm = D @ (A + np.eye(n, dtype=np.float32)) @ D
    return X, Anorm

class GCN(nn.Module):
    def __init__(self, fin=4, hid=32):
        super().__init__()
        self.w1 = nn.Linear(fin, hid)
        self.w2 = nn.Linear(hid, hid)
        self.head = nn.Linear(hid, 1)

    def forward(self, X, A):
        h = torch.relu(A @ self.w1(X))
        h = torch.relu(A @ self.w2(h))
        return self.head(h.mean(0)).squeeze()

def run():
    pos_t = json.load(open("data/ml/Tdohrnii_pos.json"))
    pos_a = json.load(open("data/ml/Aaurita_pos.json"))
    graphs, labels = [], []
    for s in pos_t:
        g = graph_from_seq(s)
        if g: graphs.append(g); labels.append(1)
    for s in pos_a:
        g = graph_from_seq(s)
        if g: graphs.append(g); labels.append(0)
    y = np.array(labels)
    n = len(y)
    # baseline k-mer LR
    Xk = np.stack([kmer_vector(s, k=6) for s in pos_t + pos_a])
    yk = np.array([1]*len(pos_t) + [0]*len(pos_a))
    rng = np.random.default_rng(0)
    gnn_aucs, lr_aucs = [], []
    for seed in range(5):
        idx = rng.permutation(n)
        folds = np.array_split(idx, 5)
        for f in folds:
            te = f
            tr = np.setdiff1d(idx, te)
            torch.manual_seed(seed)
            model = GCN()
            opt = torch.optim.Adam(model.parameters(), lr=5e-3)
            lossf = nn.BCEWithLogitsLoss()
            model.train()
            for ep in range(40):
                tot = 0
                for i in tr:
                    X, A = graphs[i]
                    Xt = torch.tensor(X); At = torch.tensor(A)
                    opt.zero_grad()
                    out = model(Xt, At)
                    loss = lossf(out, torch.tensor(float(y[i])))
                    loss.backward()
                    opt.step()
            model.eval()
            scores = []
            with torch.no_grad():
                for i in te:
                    X, A = graphs[i]
                    scores.append(float(torch.sigmoid(model(torch.tensor(X), torch.tensor(A)))))
            gnn_aucs.append(float(roc_auc_score(y[te], scores)))
            lr = LogisticRegression(max_iter=1000).fit(Xk[tr], yk[tr])
            lr_aucs.append(float(roc_auc_score(yk[te], lr.predict_proba(Xk[te])[:, 1])))
    out = {"task": "Tdohrnii vs Aaurita upstream discrimination (positives)",
           "n_tdohrnii": len(pos_t), "n_aaurita": len(pos_a),
           "gnn_auroc_mean": float(np.mean(gnn_aucs)), "gnn_auroc_sd": float(np.std(gnn_aucs)),
           "kmer_lr_auroc_mean": float(np.mean(lr_aucs)), "kmer_lr_auroc_sd": float(np.std(lr_aucs))}
    json.dump(out, open("results/ml_gnn.json", "w"), indent=1)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    run()
