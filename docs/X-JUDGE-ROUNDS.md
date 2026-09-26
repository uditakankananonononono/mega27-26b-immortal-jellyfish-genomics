# Judge rounds for the 26b expansion (user rule 2, min 10, weakness-focused)
Started 2026-09-26. Each round: scope, weakness found, fix, evidence.
Route CONFIRMED by main (4:12): cloud browser on the user's own ChatGPT
account (she explicitly ordered 'ask CHATGPT' 4:11:18). Verbatim prompt and
response logged per round; fixes implemented with evidence. Rule 6 (4:12:25):
when a negative stops moving forward, ask ChatGPT for redirection and pivot
on the strongest option, verbatim logs. Rounds focus on weaknesses and what
to add; judges never redefine locked gates after outcomes.

R1 (pipeline integrity): scheduled after mapping completes.
R2 (statistics correctness): scheduled after x_stats.
R3 (panel composition bias).
R4 (assembly-quality confounds).
R5 (control sufficiency).
R6 (paper claims vs evidence).
R7 (page-rule compliance + completeness).
R8 (reproducibility from clean checkout).
R9 (aging-routing strength).
R10 (neurology-routing strength).
R11+ (weaknesses found by R1-R10).

## Rule 8 (user 5:00:38 PM): novelty fold-back requirement
Per-round log format is now: (1) verbatim prompt, (2) verbatim response, (3) the critique extracted,
(4) the CONCRETE NOVELTY CHANGE implemented in response (file/commit reference), (5) round counts
toward the 10 only if (4) is non-empty and actually landed in the repo.
