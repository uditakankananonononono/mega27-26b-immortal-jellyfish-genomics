"""CNN upstream classifier + k-mer baseline + cross-species transfer.

Within-species: 5-fold CV, 5 seeds, AUROC (CNN vs 6-mer logistic baseline).
Transfer: train on one jellyfish, test on the other (both directions).
Prediction from the motif arm: within-species works, cross-species transfer
fails toward chance if upstream vocabularies are truly divergent.
Output: results/ml_cnn.json
"""
import json, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jellyfish.ml import one_hot, kmer_vector, build_xy, kfold_indices
import torch
from torch import nn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

torch.manual_seed(0)

class SmallCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(4, 16, 9, padding=4), nn.ReLU(), nn.MaxPool1d(4),
            nn.Conv1d(16, 32, 7, padding=3), nn.ReLU(), nn.MaxPool1d(4),
            nn.Flatten(), nn.Linear(32 * 125, 32), nn.ReLU(), nn.Linear(32, 1))

    def forward(self, x):
        return self.net(x).squeeze(-1)

def train_cnn(Xtr, ytr, Xte, seed, epochs=25):
    torch.manual_seed(seed)
    model = SmallCNN()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    lossf = nn.BCEWithLogitsLoss()
    Xtr_t = torch.tensor(Xtr, dtype=torch.float32)
    ytr_t = torch.tensor(ytr, dtype=torch.float32)
    Xte_t = torch.tensor(Xte, dtype=torch.float32)
    model.train()
    for ep in range(epochs):
        opt.zero_grad()
        out = model(Xtr_t)
        loss = lossf(out, ytr_t)
        loss.backward()
        opt.step()
    model.eval()
    with torch.no_grad():
        return torch.sigmoid(model(Xte_t)).numpy()

def auroc(y, s):
    return float(roc_auc_score(y, s)) if len(set(y)) > 1 else None

def main():
    data = {}
    for g in ("Tdohrnii", "Aaurita"):
        pos = json.load(open(f"data/ml/{g}_pos.json"))
        neg = json.load(open(f"data/ml/{g}_neg.json"))
        data[g] = (pos, neg)
    results = {"within_species": {}, "transfer": {}}
    # within-species CV
    for g, (pos, neg) in data.items():
        X_img, y = build_xy(pos, neg, one_hot)
        X_km, _ = build_xy(pos, neg, kmer_vector, k=6)
        cnn_aucs, km_aucs = [], []
        for seed in range(5):
            for tr, te in kfold_indices(len(y), k=5, seed=seed):
                s = train_cnn(X_img[tr], y[tr], X_img[te], seed)
                cnn_aucs.append(auroc(y[te], s))
                lr = LogisticRegression(max_iter=1000).fit(X_km[tr], y[tr])
                km_aucs.append(auroc(y[te], lr.predict_proba(X_km[te])[:, 1]))
        results["within_species"][g] = {
            "cnn_auroc_mean": float(np.mean(cnn_aucs)), "cnn_auroc_sd": float(np.std(cnn_aucs)),
            "kmer_lr_auroc_mean": float(np.mean(km_aucs)), "kmer_lr_auroc_sd": float(np.std(km_aucs)),
            "n_pos": len(pos), "n_neg": len(neg)}
        print(g, "within done", flush=True)
    # transfer
    for src, dst in (("Tdohrnii", "Aaurita"), ("Aaurita", "Tdohrnii")):
        pos_s, neg_s = data[src]
        pos_d, neg_d = data[dst]
        Xs_img, ys = build_xy(pos_s, neg_s, one_hot)
        Xd_img, yd = build_xy(pos_d, neg_d, one_hot)
        Xs_km, _ = build_xy(pos_s, neg_s, kmer_vector, k=6)
        Xd_km, _ = build_xy(pos_d, neg_d, kmer_vector, k=6)
        cnn_aucs, km_aucs = [], []
        for seed in range(5):
            s = train_cnn(Xs_img, ys, Xd_img, seed, epochs=30)
            cnn_aucs.append(auroc(yd, s))
            lr = LogisticRegression(max_iter=1000).fit(Xs_km, ys)
            km_aucs.append(auroc(yd, lr.predict_proba(Xd_km)[:, 1]))
        results["transfer"][f"{src}_to_{dst}"] = {
            "cnn_auroc_mean": float(np.mean(cnn_aucs)), "cnn_auroc_sd": float(np.std(cnn_aucs)),
            "kmer_lr_auroc_mean": float(np.mean(km_aucs)), "kmer_lr_auroc_sd": float(np.std(km_aucs))}
        print(src, "->", dst, "done", flush=True)
    json.dump(results, open("results/ml_cnn.json", "w"), indent=1)

if __name__ == "__main__":
    main()
