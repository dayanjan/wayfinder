# Round 2 — Claude's revision (accept / reject / defer per round-1 finding)

I accepted **all 10** round-1 findings. Two (F-001, F-002) I addressed with a **code change + re-run**
(local + Claude Science, delta-0 preserved), not a hedge; the rest are prose/scope fixes. No pushbacks.

**F-001 — Control-2 mechanism overreach. ACCEPTED (data fix).** I extended `sensitivity_panel.py` to
compute the decomposition you asked for — mean distinct C-diseases per *passing* gene, true vs. shuffled.
The result: **2.39 (true) vs. 2.44 (null)** — the per-gene concentration effect is *real but weak*, so it
does **not** carry the observed<null direction on its own. I removed the "concentrate on fewer diseases per
gene" causal sentence and now report the decomposition figure explicitly while stating the direction is a
modest consequence of the 12-disease restriction interacting with the permutation, on which we "do not
build an argument." The load-bearing claims are now only the two the shuffle actually supports:
substrate-inherited stringency + label-dependence.

**F-002 — empirical_p tail mismatch. ACCEPTED (data fix).** The script now emits `signed_z = −5.645`,
`empirical_p_upper = 1.0`, `empirical_p_lower = 0.0005`, `empirical_p_two_sided = 0.001`. The prose now
says "5.6 SD below the null (lower-tail permutation p ≈ 5×10⁻⁴; the upper-tail p is 1.0 — the hop does not
pass *more* often than chance)". A hostile reader opening the JSON now sees all three tails, and the word
"significant" is tied to the lower-tail p, not the upper-tail 1.0.

**F-003 — heading credits discrimination. ACCEPTED.** Retitled to "the disease hop's stringency is
substrate-inherited, and its pass count is label-dependent"; dropped "rubber stamp"; the §4 overview line
now says the controls "probe how much of that discrimination is a property of the data versus an artifact …
with one control returning a deliberately honest, non-obvious answer."

**F-004 — "validated" own-goal in §4.3. ACCEPTED.** "polarity marker-validated" → "polarity
marker-checked". Banned-word grep of §1/§4 now returns only the draft-note rule statements and the §4.5
lines that *quote* the flagged words as the self-audit's targets (correct usage).

**F-005 — locus-artifact language overruns the LD caveat. ACCEPTED.** §4.6 now scopes the rejection to the
"*cluster-membership* locus artifact … though not the distinct question of whether the GWAS disease *label*
is LD-inherited from the 12q13 atopy locus, which the substrate cannot settle and which we leave open".

**F-006 — "every headline number reproduced" overstates per-agent scope. ACCEPTED.** Now "Across the lab,
every headline number was independently reproduced to the unit — not every member re-checked every number,
but each number was re-derived from the raw CSVs by at least one clean-room member".

**F-007 — "five results" miscount. ACCEPTED.** Changed to "six results" (parts: 4.1+4.1b · 4.2 · 4.3 ·
4.4 · 4.5 · 4.6).

**F-008 — §1 says "proves". ACCEPTED.** "the disease hop's stringency *proves* largely inherited" → "*is*
largely inherited". (This was introduced by my own §1 softening edit — good catch.)

**F-009 — "§4.1b supplies the rate" underspecified. ACCEPTED.** Now "supplies a disease-hop support-*rate*
control over the full A×C space — not a ledger accuracy rate, nor a claim of precision or recall".

**F-010 — §4.4 corroboration traceability. ACCEPTED.** The three corroborations are now explicitly labelled
"drawn from the study's own QC fields and our finding analysis rather than the genome-wide DE row above".

**Provenance note:** the enhanced panel was re-run in Claude Science; the primary numbers (406, 467.7±10.9,
NAB2 rank 1–8) are unchanged (the seeded RNG sequence was preserved), and the new fields reproduce
byte-identically — the delta-0 dogfood claim still holds for the updated artifact.

**Preserve-intent check:** none of the three protected claims was sanded. The falsification thesis is intact;
the Control-2 honesty was *sharpened* (weaker mechanism claim, correct tails) not softened into a false
positive; the role/model/checkpoint self-audit framing is unchanged. If anything the section is now more
conservative about what the disease-hop control demonstrates.

**For round 3, please stress:** (a) is the Control-2 rewrite now correctly scoped on *both* tails, or does
"label-dependent" still over-read a lower-tail-only effect? (b) any remaining number that does not trace to
a primary artifact? (c) whole-paper consistency (§1–§4) on the disease-hop framing.
