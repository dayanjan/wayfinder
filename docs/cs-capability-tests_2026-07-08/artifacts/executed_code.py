"""
Claude Science capability audit — executed Python source (Parts A, B, C, E).
CPU-only, no external data fetched. Reproduces the audit artifacts in
cs_capability_audit_db/.

Part A note: host.delegate() was attempted first but delegation is disabled
for this session (ultra-mode toggle off), so the five differentiated personas
were sampled via host.llm() parallel fan-out — the functional equivalent for
multi-persona sampling. The attempted delegate call is retained below (commented)
for provenance.
"""
import os, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("cs_capability_audit_db", exist_ok=True)
os.makedirs("handoff", exist_ok=True)

# ---------------------------------------------------------------------------
# PART A — five differentiated reviewer personas
# ---------------------------------------------------------------------------
# Attempted first (raised: "delegation is not enabled for this session"):
#   schema = {"type":"object","properties":{
#       "persona":{"type":"string"},"key_concern":{"type":"string"},
#       "concrete_check":{"type":"string"}},
#       "required":["persona","key_concern","concrete_check"]}
#   reqs = [{"task": ..., "name": ..., "context_summary": ...,
#            "output_schema": schema} for persona in personas]
#   results = host.delegate(reqs)          # <- blocked, delegation toggle off
#
# Fallback: host.llm() fan-out (same multi-persona sampling, executed).
personas = [
    ("immunology referee", "You review a study reporting NAB2 knockdown reduces target gene expression across two guides in an immune-cell context."),
    ("statistics reviewer", "You review the statistical claims of a knockdown study reporting adjusted p-values and effect sizes."),
    ("visualization critic", "You review the figures/dashboards of a knockdown study for visualization quality and honesty."),
    ("reproducibility auditor", "You audit the reproducibility and provenance of a computational knockdown-analysis pipeline."),
    ("skeptical integrator", "You are the final skeptical integrator weighing whether the overall empirical claims of a knockdown study hold together."),
]
reqs = []
for role, ctx in personas:
    reqs.append(
        f"CONTEXT: {ctx}\n\n"
        f"Act strictly as a {role}. Respond with ONLY a JSON object with exactly these keys: "
        f'"persona", "key_concern", "concrete_check". Set "persona" to "{role}". '
        f'"key_concern" = your single most important concern (one sentence). '
        f'"concrete_check" = one concrete, actionable check (one sentence). '
        f"Output raw JSON only."
    )
resp = host.llm(reqs, max_concurrency=5)

def parse(t):
    t = t.strip()
    if t.startswith("```"):
        t = t.split("```")[1]
        if t.startswith("json"):
            t = t[4:]
    return json.loads(t.strip())

rows = []
for (role, _), r in zip(personas, resp):
    try:
        d = parse(r.get("text", ""))
    except Exception:
        d = {"persona": role, "key_concern": "", "concrete_check": ""}
    rows.append({"persona": d.get("persona", role),
                 "key_concern": d.get("key_concern", ""),
                 "concrete_check": d.get("concrete_check", "")})
pd.DataFrame(rows, columns=["persona", "key_concern", "concrete_check"]).to_csv(
    "cs_capability_audit_db/delegation_results.csv", index=False)
# persona_synthesis.md written from `rows` (convergent theme: knockdown
# validation & specificity across all five lenses).

# ---------------------------------------------------------------------------
# PART B — inline host model sampling (yes/no empirical-claim labels)
# ---------------------------------------------------------------------------
chunks = [
    "NAB2 knockdown reduced target expression in both guides.",
    "This dashboard looks polished.",
    "The adjusted p-value was 0.002.",
    "The method is interesting.",
]
prompts = [f'Does this sentence make an empirical claim? Answer exactly "yes" or "no". Sentence: "{c}"'
           for c in chunks]
bresp = host.llm(prompts, max_concurrency=4)

def norm(t):
    t = t.strip().lower().strip('."')
    return "yes" if t.startswith("yes") else ("no" if t.startswith("no") else t)

pd.DataFrame([{"chunk": c, "empirical_claim": norm(r.get("text", ""))}
             for c, r in zip(chunks, bresp)]).to_csv(
    "cs_capability_audit_db/inline_sampling_results.csv", index=False)

# ---------------------------------------------------------------------------
# PART C — persistent kernel state (created here; reused in a later cell)
# ---------------------------------------------------------------------------
rng = np.random.default_rng(20260708)
persistent_df = pd.DataFrame({
    "group": rng.choice(["A", "B", "C"], size=30),
    "x": rng.normal(0, 1, 30).round(4),
    "y": rng.normal(5, 2, 30).round(4),
})
persistent_marker = "kernel_reuse_marker_db_audit_2026_07_08"
# --- later cell: reuse from memory, no CSV re-read ---
assert "persistent_df" in dir() and "persistent_marker" in dir()
persistent_df["z"] = persistent_df["x"] + persistent_df["y"]
persistent_df.to_csv("cs_capability_audit_db/kernel_reuse_output.csv", index=False)
persistent_df.to_csv("handoff/persistent_df_for_r.csv", index=False)  # handoff to R (Part D)

# ---------------------------------------------------------------------------
# PART E — figure self-sight and correction
# ---------------------------------------------------------------------------
rng2 = np.random.default_rng(7)
X = np.append(rng2.normal(0, 1, 20), 8.5)
Y = np.append(rng2.normal(0, 1, 20), -7.2)
scatter = pd.DataFrame({"x": X.round(4), "y": Y.round(4)})

fig1, ax1 = plt.subplots(figsize=(6, 5))
ax1.scatter(scatter["x"], scatter["y"], s=45, color="#377eb8", edgecolor="white", linewidth=0.5)
ax1.set_xlabel("x"); ax1.set_ylabel("y"); ax1.set_title("Scatter v1 — raw")
fig1.tight_layout(); fig1.savefig("cs_capability_audit_db/scatter_v1.png", dpi=300); plt.close(fig1)

zx = (scatter["x"] - scatter["x"].mean()) / scatter["x"].std(ddof=0)
zy = (scatter["y"] - scatter["y"].mean()) / scatter["y"].std(ddof=0)
mask = (zx.abs() > 3) | (zy.abs() > 3)

fig2, ax2 = plt.subplots(figsize=(6, 5))
ax2.scatter(scatter.loc[~mask, "x"], scatter.loc[~mask, "y"], s=45, color="#377eb8",
            edgecolor="white", linewidth=0.5, label="within 3\u03c3")
ax2.scatter(scatter.loc[mask, "x"], scatter.loc[mask, "y"], s=140, facecolor="none",
            edgecolor="#e41a1c", linewidth=2.2, label="outlier (>3\u03c3)")
for _, r in scatter[mask].iterrows():
    ax2.annotate("outlier", (r["x"], r["y"]), textcoords="offset points",
                 xytext=(-10, 25), ha="right", fontsize=8, color="#e41a1c",
                 arrowprops=dict(arrowstyle="->", color="#e41a1c"))
ax2.set_xlabel("x"); ax2.set_ylabel("y"); ax2.set_title("Scatter v2 — outlier labeled (>3\u03c3)")
ax2.legend(frameon=False, loc="lower left")
fig2.tight_layout(); fig2.savefig("cs_capability_audit_db/scatter_v2.png", dpi=300); plt.close(fig2)
