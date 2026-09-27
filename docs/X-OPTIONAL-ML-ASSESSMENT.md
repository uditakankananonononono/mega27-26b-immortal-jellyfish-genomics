# P1 #9 optional ML ranker: not trained in this pass

The provided judge round describes this as optional. An honest supervised model needs a
non-circular target label and held-out examples. We have neither a validated T. dohrnii
rejuvenation-relevance label set nor adequately powered expression-change estimates.
The available AEES inputs (conservation, locus count and assembly agreement) are already
used to rank evidence, and GenAge/CellAge membership is an annotation source, not an
independent rejuvenation outcome. Training on those memberships would learn database
ascertainment and human-study bias, not jellyfish regeneration. The exploratory 1% RNA
sample is one library per stage and has fewer than ten ATG5 read ends per locus-stage;
copy count is structurally unresolved. An attractive learned score could therefore
outperform AEES against circular labels while adding no biological signal.

Decision: defer optional supervised ranking rather than report an unvalidated ML number.
The existing closed-phase CNN/GNN arms are separate tasks and are not represented as
rejuvenation relevance models. Revisit only with independent functional/replicate-aware
labels, non-leaky features and a species-held-out split. No model was trained here.
