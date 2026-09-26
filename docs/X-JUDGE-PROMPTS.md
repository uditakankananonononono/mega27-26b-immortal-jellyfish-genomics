# Prepared judge-round prompts (verbatim use in ChatGPT rounds; min 10)
Common framing prepended per round: "You are a hostile but fair ISEF judge
reviewing a computational-biology project by a high-school researcher.
Project: genome-first comparative genomics of the immortal jellyfish
Turritopsis dohrnii vs mortal cnidarians (T. rubra, A. aurita, annotated
Clytia calibration), mapping 24 aging/longevity + 24 neurodegeneration genes
with a frozen tBLASTn pipeline, positive/negative controls, pre-registered
hypotheses, honest-negative register. Attack weaknesses only; for each, say
exactly what to add or change to make the project better. Be specific."

R1 PIPELINE: "Here are the pipeline choices: tBLASTn evalue 1e-5, locus =
clustered HSPs within 50kb, strong locus >= 100 total bits, presence = >=1
strong locus, copy = #strong loci. Attack these choices for false-positive
and false-negative risk on a 436Mb draft genome."
R2 STATISTICS: "Tests: binomial vs shuffled-control FPR for mapping
fractions, Fisher exact per-gene for copy contrasts (BH), exact label
permutation for species separation, Fisher for panel overlap. Attack the
test choices, the families, and the multiple-testing boundaries."
R3 PANELS: "Panels of 24 aging + 24 neurodegeneration genes (list provided).
Attack the panel composition: survivorship bias toward famous genes, missing
categories, genes that should be added or dropped, and what that does to
inference."
R4 ASSEMBLY CONFOUNDS: "T. dohrnii assemblies are 891-contig and 74,835-
scaffold drafts; T. rubra is chromosome-level. Attack whether ANY presence or
copy contrast can be trusted given this asymmetry, and what controls would
rescue it."
R5 CONTROLS: "Controls: shuffled-query FPR per genome (criterion <=5%) and
reproduction of prior panel calls. Attack control sufficiency: what failure
modes do these controls NOT catch?"
R6 CLAIMS: [paper results chapters attached] "Attack every sentence where the
claim exceeds the evidence class (mapping vs function vs adaptation)."
R7 COMPLETENESS: "Rule: 50+ pages body text, headings/references/appendix/
diagrams excluded. Attack the paper structure for missing sections a judge
would expect (data availability, ethics, author contributions, limitations,
future work) and missing analyses."
R8 REPRODUCIBILITY: "Given a clean checkout + README, attack whether another
student could regenerate every number: where are the hidden dependencies,
versions, and manual steps?"
R9 AGING ROUTING: "The paper claims the census is useful to aging/longevity
research. Attack that claim: what would a skeptical longevity researcher say
is missing or overstated?"
R10 NEURO ROUTING: "The paper claims the census is useful to neurology.
Attack that claim: what would a skeptical neurodegeneration geneticist say
is missing or overstated?"
R6-REDIRECT (rule 6, only if a hypothesis fails and is stuck): "Hypothesis
HX failed as follows: [details]. It is not moving forward. Give ranked
redirection options that keep the same data and preregistration discipline,
and say which single pivot is strongest and why."
