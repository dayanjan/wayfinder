# Round 1 — Claude's opening position

**Artifact:** `docs/plans/heldout-eval-implementation-plan_2026-07-12.md` — a time-sliced held-out evaluation
(Option A) to convert the Wayfinder method from *demonstrated* to *measured*, closing the audit's central FATAL.

**The position.** The eval freezes literature at T=2016, regenerates the pipeline using only pre-T literature,
and measures whether Wayfinder's data-grounded ranking recovers gene→Th1/Th2→disease links that became
literature-established *after* T (novel-at-T `ac_lit_asof≤1` → established-now `ac_lit_now≥5`; ~1,469 positives
projected, spike-sized). It compares Wayfinder against four baselines (literature-rarity, effect-only,
enrichment-only, random) via precision@k, MAP, recall with bootstrap CIs.

**Defense of the two flagged risks (the framing question):**

*Q1 — referee time-invariance (is "Wayfinder" a circular leak?).* The referee's hop verdicts read the FIXED 2025
Perturb-seq tables, so they do not change with T. This is deliberate and is the SIGNAL, not a leak: the eval's
whole hypothesis is that *fixed experimental data* "knows" biology the literature has not yet written down, so
data-grounding should predict future literature better than literature-rarity. It is only a leak if the
*outcome labels* (future literature) were derived from the same tables — they are NOT (labels come from Europe
PMC co-mention growth, independent of the perturbation data). The referee never sees the future-literature label.
So the comparison is fair: both Wayfinder and the baselines rank the SAME as-of-T-eligible candidates; only their
ranking signal differs (data+referee vs literature-rarity vs single data axes). If the data signal wins, that is
a real result; if it doesn't, we report the null.

*Q2 — dropping `ac_known`.* Open Targets association is current-only (no as-of-T API); keeping it would exclude
exactly the links that later became known (the positives), biasing AGAINST finding signal. Dropping it is the
conservative choice and is applied symmetrically (Wayfinder's `ac_known` term = 0; no baseline uses it). The
sliced funnel therefore differs slightly from the headline funnel; we report both.

**What is genuinely uncertain (invite attack):** whether precision@k is the right primary metric at ~6.7%
positives (vs MAP / PR-AUC); whether the as-of-T `ab`/`bc` recomputation + gate can shrink the positive frame
below the power floor (a build-time re-size checkpoint guards this); whether CS-native execution of a live
date-windowed sweep is feasible or whether local execution (honestly stated) is sufficient.

**Preserve-intent (do not sand):** the novel claim is *"a fixed experimental substrate predicts which currently-
novel links become literature-established later, better than literature-rarity — and we commit to reporting a
null straight."* Prefer "open question / test it" over "agree it won't work."
