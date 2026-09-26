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

## RULE 7 update (2026-09-26, user 4:14:37 via main): ISEF-winner archetypes

Verified winner template (Society for Science official abstract, project 23691, Regeneron ISEF 2023,
https://abstracts.societyforscience.org/Home/FullAbstract?AllAbstracts=False&Category=Biomedical+and+Health+Sciences&FairCountry=Any+Country&FairState=Any+State&ISEFYears=0%2C&ProjectId=23691):
Natasha Kulviwat (Jericho High School), "The Neurobiology of Suicide: Claudin-5 Is a Novel Biomarker
of Suicide Pathogenesis" - Gordon E. Moore Award + First Award ($5,000, LISEF special-awards PDF).
Archetype elements: (1) nominate a specific novel biomarker where none existed; (2) verify with
independent human evidence (postmortem brain cohort stratified by outcome); (3) stack orthogonal
assays (ELISA, immunolocalization, public RNA-seq DE + pathway enrichment); (4) translational arm
(docking of current drugs against the biomarker); (5) pre-marker/clinical framing.

Mapping of this project to the archetype: the "biomarker" = a named gene/locus set whose genomic
presence or copy pattern distinguishes T. dohrnii from mortal relatives; "independent human
evidence" = the frozen human-derived queries themselves plus second-assembly replication; orthogonal
assays = shuffled-control FPR, Clytia calibration, panel-vs-panel contrasts; translational arm =
mapped genes that are druggable aging/neuro targets. What the archetype says is missing and must be
answered in results/discussion: NAME a top candidate biomarker (not only statistics), give it a
falsifiable validation plan, and state the human-health translation path explicitly.

R7 WINNER-ARCHETYPE round (new judge-round template):
"You know the ISEF winner archetype of biomarker identification + multi-assay verification +
translational endpoint (e.g. Kulviwat ISEF 2023, claudin-5 suicide biomarker: postmortem human
cohort, orthogonal assays, drug docking). Here is this project's results chapter. What would a
judge who knows that winner say is missing here? What single addition would make this project feel
like that class of work? Be specific and ruthless."

## RULE 8 update (2026-09-26, user 5:00:38 PM, wamid.HBgMOTE4MTM0MDk4NTcxFQIAEhgWM0VCMEJGMEMxMkZCNThFNzczQkJCRQA= verified in phone_messages):
Every judge round must IMPROVE PROJECT NOVELTY. A round counts toward the 10-round minimum ONLY
if its output is folded back into the work as a concrete novelty improvement (novel angle, method,
analysis, or feature added in response) - critique alone does not count.
