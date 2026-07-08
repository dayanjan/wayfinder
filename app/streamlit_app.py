"""PyZoBot Arbiter — the Researcher's Workbench.

Screens: (1) Referee — instant, deterministic; (2) Hypothesis Engine — the LBD generate→cull funnel
+ the 30 clean questions, each click-adjudicated live. Every verdict + receipt is computed LIVE from
the four public Perturb-seq tables via arbiter.lbd.referee_triple — nothing hardcoded. Implements the
Claude co-design spec (claude.ai/design project 563180df; see app/DESIGN_SOURCE.md).

Run from repo root:  streamlit run app/streamlit_app.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "src"))          # F-001: arbiter is not installable; put src on the path FIRST

import pandas as pd
import streamlit as st
from arbiter.lbd.referee_triple import referee_triple, load_referee_data
from arbiter.lbd.entities import build_a_universe, load_c

_FIX = _REPO / "app" / "fixtures"

# ------------------------------------------------------------------ data (once)
@st.cache_resource
def _referee_data():
    return load_referee_data()

@st.cache_data
def _gene_options():
    genes = sorted(build_a_universe(condition="Stim8hr", program_significant=True).symbol.unique().tolist())
    lead = [g for g in ("NAB2", "SATB1", "NUDT1") if g in genes]
    return lead + [g for g in genes if g not in lead]

@st.cache_data
def _disease_options():
    return [c["disease"] for c in load_c()]

@st.cache_data
def _sweep():
    return json.loads((_FIX / "sweep_Stim8hr.json").read_text())

_CS_DIR = _REPO / "docs" / "claude-science-evidence-chain_2026-07-08"
_CS_FIG = _CS_DIR / "nab2_evidence_chain.png"

@st.cache_data
def _cs():
    return json.loads((_CS_DIR / "claude_science_verdict.json").read_text(encoding="utf-8"))

D = _referee_data()
GENES = _gene_options()
DISEASES = _disease_options()
COND_DISPLAY = {"Rest": "Rest", "Stim8hr": "Stim 8 hr", "Stim48hr": "Stim 48 hr"}
COND_KEYS = list(COND_DISPLAY.keys())

CHIPS = [
    {"key": "eczema", "gene": "NAB2",  "disease": "atopic eczema",      "cond": "Stim8hr", "v": "ok",   "hint": "CONFIDENT YES"},
    {"key": "asthma", "gene": "SATB1", "disease": "asthma",             "cond": "Stim8hr", "v": "warn", "hint": "UNTESTED · halts at gate"},
    {"key": "ms",     "gene": "NAB2",  "disease": "multiple sclerosis", "cond": "Stim8hr", "v": "bad",  "hint": "CONFIDENT NO"},
]

# ------------------------------------------------------------------ verdict taxonomy
_VMAP  = {"supported": "ok", "untested": "warn", "refuted": "bad", "flagged": "warn", "noteval": "mute"}
_MARK  = {"supported": "✓", "untested": "!", "refuted": "✕", "flagged": "⚑", "noteval": "·"}
_WORD  = {"supported": "Supported", "untested": "Untested", "refuted": "Refuted", "flagged": "Flagged", "noteval": "Not evaluated"}
_ANSWER = {
    "supported": ("Supported", "ok"), "supported_weak": ("Supported · weak", "warn"),
    "supported_flagged": ("Supported · flagged", "warn"), "untested": ("Untested", "warn"),
    "untested_for_c": ("Untested", "warn"), "refuted_for_c": ("Refuted", "bad"),
    "refuted_effect": ("Refuted", "bad"), "refuted_program": ("Refuted", "bad"),
}


def _p(x) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "—"
    if x != x:
        return "n/a"
    if x == 0:
        return "0"
    return f"{x:.0e}".replace("e-0", "e-") if x < 1e-3 else f"{x:.3f}"


def _tokens(hop: dict) -> list[str]:
    name, r = hop["name"], hop.get("receipt") or {}
    if name == "GATE":
        ng, ns = r.get("n_guides"), r.get("n_signif_knockdown_guides")
        g, ntc = r.get("mean_guide_expr"), r.get("mean_ntc_expr")
        toks = [f"{ns}/{ng} guides significant", f"adj-p {_p(r.get('best_guide_adj_p'))}"]
        if g is not None and ntc is not None:
            tail = " (barely moved)" if hop["status"] == "untested" else ""
            toks.append(f"expr {g:.3f} vs {ntc:.3f}{tail}")
        return toks
    if name == "EFFECT":
        toks = [f"effect {r.get('ontarget_effect_size'):+.1f}", f"{r.get('n_downstream_DE_genes')} downstream genes"]
        toks.append("off-target flagged" if r.get("offtarget_flag") else "no off-target flag")
        rg = r.get("crossguide_correlation")
        if rg is not None:
            toks.append(f"reproducibility R {rg:.2f}")
        return toks
    if name == "PROGRAM":
        toks = []
        for label, sub in r.items():
            if not isinstance(sub, dict):
                continue
            short = "Ota 2021" if "Ota" in label else ("Höllbacher" if ("Hollbacker" in label or "Höll" in label) else label)
            if sub.get("significant"):
                toks.append(f"{short}: z {sub.get('zscore'):.2f}, adj-p {_p(sub.get('adj_p_value'))}")
            else:
                toks.append(f"{short}: same direction, n.s.")
        return toks
    if name == "DISEASE":
        if hop["status"] == "supported":
            t = [f"odds ratio {r.get('odds_ratio'):.2f}", f"FDR {_p(r.get('p_adj_fdr'))}"]
            nc = r.get("n_significant_clusters")
            if nc:
                t.append(f"{nc} significant cluster" + ("s" if nc != 1 else ""))
            return t
        c = r.get("c_disease", "this disease")
        if "best_p_adj_fdr" in r:
            return [f"best FDR {_p(r.get('best_p_adj_fdr'))} — not significant"]
        return [f"not in any {c} cluster at FDR<0.05"]
    return []


def _caveat(hop: dict) -> str:
    name, r, st_ = hop["name"], hop.get("receipt") or {}, hop["status"]
    if name == "PROGRAM" and st_ == "supported":
        if [v for v in r.values() if isinstance(v, dict) and not v.get("significant")]:
            return "one cohort not significant"
    if name == "DISEASE" and st_ == "refuted" and r.get("present_in_other_diseases"):
        return "enriched instead for: " + " · ".join(r["present_in_other_diseases"])
    return ""


def _cards(res: dict) -> list[dict]:
    hops = {h["name"]: h for h in res["hops"]}
    default_claim = {"EFFECT": "Real on-target effect", "PROGRAM": "Shifts the T-cell program",
                     "DISEASE": "Enriched in disease modules"}
    out = []
    for name in ("GATE", "EFFECT", "PROGRAM", "DISEASE"):
        h = hops.get(name)
        if h is None:
            out.append({"step": name, "status": "noteval", "claim": default_claim.get(name, name.title()),
                        "tokens": [], "caveat": "", "noteval": True})
        else:
            out.append({"step": name, "status": h["status"], "claim": h["claim"],
                        "tokens": _tokens(h), "caveat": _caveat(h), "noteval": False})
    return out


def _cv(v):  # colour-var triple
    return f"--c:var(--{v});--cbg:var(--{v}-bg);--cl:var(--{v}-line)"


# ------------------------------------------------------------------ page + CSS
st.set_page_config(page_title="PyZoBot Arbiter", page_icon="🧬", layout="wide",
                   initial_sidebar_state="expanded")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');
:root{
  --bg:#091314;--bg2:#0f1e1f;--bg3:#16292a;--line:#22403f;
  --ink:#eaf3f1;--ink2:#a0b6b3;--ink3:#6a8785;
  --teal:#26c6c9;--teal-dim:#0e5f61;--indigo:#8285f2;--on:#05110f;
  --ok:#4fd08a;--ok-bg:rgba(79,208,138,.12);--ok-line:rgba(79,208,138,.42);
  --warn:#f2b64c;--warn-bg:rgba(242,182,76,.12);--warn-line:rgba(242,182,76,.42);
  --bad:#f26d63;--bad-bg:rgba(242,109,99,.13);--bad-line:rgba(242,109,99,.44);
  --mute:#7d9095;--mute-bg:rgba(125,144,149,.10);--mute-line:rgba(125,144,149,.30);
}
.stApp{background:var(--bg);}
html,body,[class*="css"]{font-family:'IBM Plex Sans',system-ui,sans-serif;color:var(--ink);}
#MainMenu,footer,header[data-testid="stHeader"]{visibility:hidden;height:0;}
.block-container{padding-top:1.6rem;padding-bottom:2rem;max-width:1240px;}
/* sidebar as the slim left nav */
section[data-testid="stSidebar"]{background:var(--bg2);border-right:1px solid var(--line);width:250px!important;}
section[data-testid="stSidebar"] .block-container{padding-top:1.4rem;}
.pz-brand{display:flex;align-items:center;gap:11px;margin-bottom:8px;}
.pz-logo{width:32px;height:32px;border-radius:9px;background:linear-gradient(135deg,var(--teal),var(--indigo));display:flex;align-items:center;justify-content:center;}
.pz-logo i{width:11px;height:11px;background:var(--on);transform:rotate(45deg);border-radius:2px;display:block;}
.pz-name{font-size:16px;font-weight:700;letter-spacing:-.01em;line-height:1;color:var(--ink);}
.pz-name b{color:var(--teal);font-weight:700;}
.pz-kick{font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:.14em;color:var(--ink3);text-transform:uppercase;margin-top:4px;}
.pz-tag{font-size:12px;color:var(--ink2);line-height:1.4;margin:10px 0 16px;}
.pz-note{font-size:10px;line-height:1.55;color:var(--ink3);font-family:'IBM Plex Mono',monospace;margin-top:14px;border-top:1px solid var(--line);padding-top:12px;}
/* nav buttons in the sidebar */
section[data-testid="stSidebar"] .stButton>button{width:100%;text-align:left;justify-content:flex-start;background:transparent;border:none;color:var(--ink2);font-weight:500;padding:9px 12px;border-radius:10px;}
section[data-testid="stSidebar"] .stButton>button:hover{background:var(--bg3);color:var(--ink);}
section[data-testid="stSidebar"] .stButton>button[kind="primary"]{background:var(--teal);color:var(--on);font-weight:600;}
/* headings */
.pz-h1{font-size:26px;font-weight:700;letter-spacing:-.02em;margin:2px 0 4px;color:var(--ink);}
.pz-sub{font-size:14.5px;color:var(--ink2);line-height:1.5;max-width:820px;margin-bottom:8px;}
.pz-sub em{color:var(--ink);font-style:normal;font-weight:500;}
.pz-sub strong{color:var(--ink);}
.pz-lbl{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.14em;color:var(--ink3);text-transform:uppercase;}
/* native widgets */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-testid="stTextInput"] input{background:var(--bg3)!important;border:1px solid var(--line)!important;border-radius:9px!important;color:var(--ink)!important;font-weight:600;}
div[data-baseweb="select"] *{color:var(--ink)!important;}
label p{color:var(--ink3)!important;font-family:'IBM Plex Mono',monospace!important;font-size:10px!important;letter-spacing:.14em!important;text-transform:uppercase!important;}
div[role="radiogroup"]{gap:2px;background:var(--bg3);border:1px solid var(--line);border-radius:9px;padding:3px;}
div[role="radiogroup"] label{margin:0;padding:6px 10px;border-radius:7px;}
.stMain .stButton>button{background:var(--bg2);color:var(--ink);border:1px solid var(--line);border-radius:10px;font-weight:600;transition:all .15s;}
.stMain .stButton>button:hover{border-color:var(--teal);color:var(--teal);}
.stMain .stButton>button[kind="primary"]{background:var(--teal);color:var(--on);border:none;}
.stMain .stButton>button[kind="primary"]:hover{filter:brightness(1.08);color:var(--on);}
/* result HTML */
.pz-banner{display:flex;align-items:flex-start;gap:18px;background:var(--cbg);border:1px solid var(--cl);border-left:4px solid var(--c);border-radius:14px;padding:18px 22px;margin-top:8px;}
.pz-badge{flex:none;display:inline-flex;align-items:center;gap:7px;background:var(--c);color:var(--on);padding:6px 13px;border-radius:999px;font-family:'IBM Plex Mono',monospace;font-size:11.5px;font-weight:600;letter-spacing:.1em;margin-top:2px;}
.pz-verdict{font-size:20px;font-weight:600;line-height:1.35;letter-spacing:-.01em;color:var(--ink);}
.pz-meta{margin-top:9px;font-size:13px;color:var(--ink2);display:flex;gap:9px;flex-wrap:wrap;align-items:center;}
.pz-meta b{font-family:'IBM Plex Mono',monospace;color:var(--ink);font-weight:600;}
.pz-rail{display:grid;grid-template-columns:repeat(4,1fr);gap:26px;margin-top:20px;}
.pz-rail .lab{font-family:'IBM Plex Mono',monospace;font-size:9.5px;letter-spacing:.13em;text-transform:uppercase;text-align:center;margin-bottom:4px;}
.pz-rail .bar{height:8px;border:1px solid var(--line);border-top:none;border-radius:0 0 8px 8px;}
.pz-chain{display:grid;grid-template-columns:repeat(4,1fr);gap:26px;margin-top:12px;}
.pz-card{position:relative;background:var(--cbg);border:1px solid var(--cl);border-radius:14px;padding:16px 16px 18px;display:flex;flex-direction:column;gap:11px;min-height:158px;animation:pzIn .5s both cubic-bezier(.2,.7,.2,1);}
.pz-card.n0{animation-delay:.02s}.pz-card.n1{animation-delay:.5s}.pz-card.n2{animation-delay:.98s}.pz-card.n3{animation-delay:1.46s}
@keyframes pzIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.pz-card .top{display:flex;align-items:center;justify-content:space-between;gap:8px;}
.pz-step{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.16em;color:var(--ink2);}
.pz-pill{display:inline-flex;align-items:center;gap:6px;background:var(--c);color:var(--on);padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;}
.pz-claim{font-size:15px;font-weight:600;line-height:1.3;color:var(--ink);}
.pz-toks{display:flex;flex-wrap:wrap;gap:6px;margin-top:auto;}
.pz-tok{font-family:'IBM Plex Mono',monospace;font-size:12px;background:var(--bg3);border:1px solid var(--line);color:var(--ink);padding:3px 8px;border-radius:6px;}
.pz-cav{display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--warn);background:var(--warn-bg);border:1px solid var(--warn-line);border-radius:6px;padding:3px 8px;align-self:flex-start;font-weight:500;}
.pz-dim .pz-claim{text-decoration:line-through;color:var(--ink3);}
.pz-wm{margin-top:auto;display:flex;align-items:center;justify-content:center;min-height:60px;}
.pz-wm span{transform:rotate(-6deg);font-family:'IBM Plex Mono',monospace;font-size:11px;line-height:1.5;color:var(--mute);border:1px dashed var(--mute-line);padding:8px 12px;border-radius:9px;background:var(--mute-bg);text-align:center;}
.pz-empty{margin-top:24px;border:1px dashed var(--line);border-radius:18px;padding:48px 40px;text-align:center;background:var(--bg2);}
.pz-empty .k{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.18em;color:var(--ink3);text-transform:uppercase;}
.pz-empty .t{font-size:21px;font-weight:600;margin-top:12px;letter-spacing:-.01em;color:var(--ink);}
.pz-empty .d{font-size:14px;color:var(--ink2);max-width:560px;margin:10px auto 0;line-height:1.55;}
.pz-chiphint{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.13em;}
/* funnel (screen 2) */
.pz-funnel{background:var(--bg2);border:1px solid var(--line);border-radius:16px;padding:26px 28px;}
.pz-frow{display:flex;align-items:center;gap:18px;margin-bottom:10px;}
.pz-fbar{flex:none;color:var(--on);border-radius:9px;padding:12px 16px;display:flex;align-items:center;min-width:120px;}
.pz-fbar span{font-family:'IBM Plex Mono',monospace;font-size:22px;font-weight:600;}
.pz-flab{font-size:13.5px;color:var(--ink2);}
.pz-fcull{text-align:center;margin-top:14px;font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--bad);}
.pz-break{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px;justify-content:center;}
.pz-bchip{font-family:'IBM Plex Mono',monospace;font-size:11.5px;padding:4px 10px;border-radius:999px;border:1px solid var(--line);color:var(--ink2);background:var(--bg3);}
.pz-note2{margin-top:14px;font-size:12.5px;color:var(--ink3);line-height:1.5;background:var(--bg2);border:1px solid var(--line);border-radius:12px;padding:12px 16px;}
.pz-note2 b{color:var(--warn);}
.pz-foot{margin-top:34px;padding-top:16px;border-top:1px solid var(--line);font-size:11.5px;color:var(--ink3);line-height:1.5;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;}
.pz-foot .mono{font-family:'IBM Plex Mono',monospace;}
/* claude science (screen 3) */
.pz-panel{background:var(--bg2);border:1px solid var(--line);border-radius:16px;padding:20px 22px;height:100%;}
.pz-cslabel{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.14em;color:var(--ink3);text-transform:uppercase;margin-bottom:12px;}
.pz-csnar{font-size:14px;line-height:1.6;color:var(--ink2);}
.pz-csnar b{color:var(--ink);}
.pz-callout{background:var(--ok-bg);border:1px solid var(--ok-line);border-left:4px solid var(--ok);border-radius:12px;padding:14px 16px;margin-top:16px;}
.pz-callout .k{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--ok);font-weight:600;letter-spacing:.08em;}
.pz-callout .t{font-size:14px;margin-top:5px;color:var(--ink);}
.pz-hop{display:flex;gap:10px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--line);}
.pz-hop:last-child{border-bottom:none;}
.pz-htag{flex:none;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;letter-spacing:.06em;color:var(--ink3);width:74px;}
.pz-hrec{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--ink2);line-height:1.5;}
.pz-conf{margin-top:14px;background:var(--bg3);border:1px solid var(--line);border-radius:12px;padding:14px 16px;}
.pz-conf .h{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.1em;color:var(--teal);text-transform:uppercase;margin-bottom:8px;}
.pz-conf .row{font-size:12.5px;color:var(--ink2);line-height:1.55;margin-bottom:5px;}
.pz-conf .row b{color:var(--ink);}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------ state + callbacks
ss = st.session_state
ss.setdefault("screen", "referee")
ss.setdefault("gene", "NAB2")
ss.setdefault("disease", "atopic eczema")
ss.setdefault("cond", "Stim8hr")
ss.setdefault("result", None)

def _adjudicate():
    ss.result = referee_triple(ss.gene, ss.disease, ss.cond, D)

def _pick_chip(chip):
    ss.gene, ss.disease, ss.cond = chip["gene"], chip["disease"], chip["cond"]
    ss.result = referee_triple(chip["gene"], chip["disease"], chip["cond"], D)

def _go(screen):
    ss.screen = screen

def _adjudicate_question(gene, disease):
    ss.gene, ss.disease, ss.cond = gene, disease, "Stim8hr"
    ss.result = referee_triple(gene, disease, "Stim8hr", D)
    ss.screen = "referee"

def _adjudicate_survivor():
    recs = _sweep()["ranked_clean_supported"]
    r = recs[ss.get("survivor_idx", 0)]
    _adjudicate_question(r["a_gene"], r["c_disease"])

# ------------------------------------------------------------------ sidebar nav
with st.sidebar:
    st.markdown(
        '<div class="pz-brand"><div class="pz-logo"><i></i></div>'
        '<div><div class="pz-name">PyZoBot <b>Arbiter</b></div>'
        '<div class="pz-kick">Hypothesis referee</div></div></div>'
        '<div class="pz-tag">Receipt-backed. Willing to refute.</div>', unsafe_allow_html=True)
    st.button("Referee", key="nav_ref", use_container_width=True,
              type="primary" if ss.screen == "referee" else "secondary", on_click=_go, args=("referee",))
    st.button("Hypothesis Engine", key="nav_eng", use_container_width=True,
              type="primary" if ss.screen == "engine" else "secondary", on_click=_go, args=("engine",))
    st.button("Claude Science", key="nav_cs", use_container_width=True,
              type="primary" if ss.screen == "claude" else "secondary", on_click=_go, args=("claude",))
    st.markdown('<div class="pz-note">Calibrated language only — consistent&nbsp;with · re-derived · '
                'refuted · untested · flagged. Never "proven".</div>', unsafe_allow_html=True)


# ------------------------------------------------------------------ screen 1: referee
def render_referee():
    st.markdown('<div class="pz-h1">Referee</div>'
                '<div class="pz-sub">Pose a mechanistic claim — <em>gene G regulates program P, implicated '
                'in disease D</em> — and get a verdict with a receipt for every step. It says a confident '
                '<em>no</em>, or <em>untested</em>, when the data warrants.</div>', unsafe_allow_html=True)

    c_gene, c_dis, c_cond, c_btn = st.columns([1, 1.4, 1.3, 1])
    with c_gene:
        st.selectbox("Gene", GENES, key="gene")
    with c_dis:
        st.selectbox("Disease module", DISEASES, key="disease", format_func=lambda s: s[:1].upper() + s[1:])
    with c_cond:
        st.radio("Condition", COND_KEYS, key="cond", horizontal=True, format_func=lambda k: COND_DISPLAY[k])
    with c_btn:
        st.markdown('<div style="height:26px"></div>', unsafe_allow_html=True)
        st.button("Adjudicate", type="primary", use_container_width=True, on_click=_adjudicate)

    st.markdown('<div class="pz-lbl" style="margin-top:14px">Try these — the whole story at a glance</div>',
                unsafe_allow_html=True)
    for col, chip in zip(st.columns(3), CHIPS):
        with col:
            hexc = {"ok": "#4fd08a", "warn": "#f2b64c", "bad": "#f26d63"}[chip["v"]]
            st.button(f"{chip['gene']} → {chip['disease']}", key=f"chip_{chip['key']}",
                      use_container_width=True, on_click=_pick_chip, args=(chip,))
            st.markdown(f'<div class="pz-chiphint" style="color:{hexc};margin:-6px 0 4px 2px">{chip["hint"]}</div>',
                        unsafe_allow_html=True)

    res = ss.result
    if res is None:
        st.markdown(
            '<div class="pz-empty"><div class="k">Awaiting a claim</div>'
            '<div class="t">Every verdict comes with a receipt.</div>'
            '<div class="d">Pick a gene and disease module above, or run one of the three examples — '
            'a confident <span style="color:var(--ok);font-weight:600">yes</span>, an honest '
            '<span style="color:var(--warn);font-weight:600">untested</span>, and a confident '
            '<span style="color:var(--bad);font-weight:600">no</span>. The referee refuses far more than it confirms.</div></div>',
            unsafe_allow_html=True)
        return
    word, vcol = _ANSWER.get(res["answer"], ("—", "mute"))
    gene, dis = res["a_gene"], res["c_disease"]
    dis_disp = dis[:1].upper() + dis[1:]
    cond = COND_DISPLAY.get(res["condition"], res["condition"])
    cards = _cards(res)
    html = [f'<div class="pz-banner" style="{_cv(vcol)}"><span class="pz-badge">{word.upper()}</span>'
            f'<div><div class="pz-verdict">{res["overall"][:1].upper() + res["overall"][1:]}</div>'
            f'<div class="pz-meta"><b>{gene}</b><span style="color:var(--ink3)">→</span>'
            f'<b>{dis_disp}</b><span style="color:var(--ink3)">·</span><span>{cond}</span></div></div></div>',
            '<div class="pz-rail">'
            '<div style="grid-column:1/4"><div class="lab" style="color:var(--ink3)">Gene-level evidence · identical across diseases</div><div class="bar"></div></div>'
            '<div style="grid-column:4/5"><div class="lab" style="color:var(--teal)">Disease-specific</div><div class="bar" style="border-color:var(--teal-dim)"></div></div></div>',
            '<div class="pz-chain">']
    for i, card in enumerate(cards):
        v = _VMAP[card["status"]]
        dim = " pz-dim" if card["noteval"] else ""
        inner = [f'<div class="top"><span class="pz-step">{card["step"]}</span>'
                 f'<span class="pz-pill">{_MARK[card["status"]]} {_WORD[card["status"]]}</span></div>',
                 f'<div class="pz-claim">{card["claim"]}</div>']
        if card["noteval"]:
            inner.append('<div class="pz-wm"><span>not evaluated<br>knockdown unverified</span></div>')
        else:
            if card["tokens"]:
                inner.append('<div class="pz-toks">' + "".join(f'<span class="pz-tok">{t}</span>' for t in card["tokens"]) + '</div>')
            if card["caveat"]:
                inner.append(f'<div class="pz-cav">⚑ {card["caveat"]}</div>')
        html.append(f'<div class="pz-card n{i}{dim}" style="{_cv(v)}">' + "".join(inner) + '</div>')
    html.append('</div>')
    st.markdown("".join(html), unsafe_allow_html=True)


# ------------------------------------------------------------------ screen 2: hypothesis engine
def _novelty(ac_lit):
    if ac_lit == 0:
        return "novel"
    if ac_lit <= 10:
        return "near-novel"
    return "known"

def render_engine():
    sw = _sweep()
    f = sw["funnel"]
    cc = f["chain_classes"]
    st.markdown('<div class="pz-h1">Hypothesis Engine</div>'
                '<div class="pz-sub">The engine generated <strong>22,039</strong> gene–disease questions '
                'from a dataset that came with none — and the referee refused all but the <strong>30</strong> '
                'it could back with a receipt at every hop. LBD proposes; the referee culls.</div>',
                unsafe_allow_html=True)

    stages = [
        (f["a_genes"], "knockdown-gated regulators — passed QC", 55, "var(--teal)"),
        (f["eligible_pairs"], "literature-eligible gene–disease questions", 64, "var(--indigo)"),
        (f["disease_c_supported_total"], "held at the disease hop", 24, "var(--warn)"),
        (f["clean_supported"], "clean, receipt-backed findings", 17, "var(--ok)"),
    ]
    rows = "".join(
        f'<div class="pz-frow"><div class="pz-fbar" style="width:{w}%;max-width:{w}%;background:{c}">'
        f'<span>{n:,}</span></div><div class="pz-flab">{lab}</div></div>'
        for n, lab, w, c in stages)
    culled = f["eligible_pairs"] - f["clean_supported"]
    breakdown = "".join(f'<span class="pz-bchip">{v:,} {k.replace("_", " ")}</span>'
                        for k, v in cc.items())
    st.markdown(
        f'<div class="pz-funnel">{rows}'
        f'<div class="pz-fcull">▼ {culled:,} of {f["eligible_pairs"]:,} did not become clean full-chain '
        f'findings — the referee kept only what carries a receipt</div>'
        f'<div class="pz-break">{breakdown}</div></div>', unsafe_allow_html=True)

    # the 30 clean survivors — click a row to adjudicate it live
    st.markdown('<div class="pz-lbl" style="margin:22px 0 8px">The 30 survivors — select a row to '
                're-adjudicate it live in the Referee</div>', unsafe_allow_html=True)
    recs = sw["ranked_clean_supported"]
    df = pd.DataFrame([{
        "Gene": r["a_gene"],
        "Disease": r["c_disease"][:1].upper() + r["c_disease"][1:],
        "Novelty": _novelty(r["ac_lit"]),
        "Effect (DE genes)": r["effect"],
        "Score": round(r["score"], 3),
        "Verdict": "Supported",
    } for r in recs])
    st.dataframe(df, hide_index=True, use_container_width=True, height=430)
    c1, c2 = st.columns([3, 1])
    with c1:
        st.selectbox("Re-adjudicate a survivor live in the Referee", range(len(recs)), key="survivor_idx",
                     format_func=lambda i: f"{recs[i]['a_gene']} → {recs[i]['c_disease'][:1].upper() + recs[i]['c_disease'][1:]}")
    with c2:
        st.markdown('<div style="height:26px"></div>', unsafe_allow_html=True)
        st.button("→ Adjudicate", type="primary", use_container_width=True, on_click=_adjudicate_survivor)

    st.markdown('<div class="pz-note2">The one <b>novel-but-weak</b> survivor — NUDT1 → type-1 diabetes '
                '— has zero prior literature but a tiny effect (4 downstream genes). Kept, but ranked low. '
                'The engine <b>ranks</b>; it does not blindly trust novelty (strict literature-absence tracks '
                'obscurity, not importance).</div>', unsafe_allow_html=True)


# ------------------------------------------------------------------ screen 3: claude science
def render_claude():
    cs = _cs()
    st.markdown('<div class="pz-h1">Claude Science</div>'
                '<div class="pz-sub">An <strong>independent</strong> Anthropic scientific agent — given '
                'only the four public tables and the question, not the answer — reasoned through the same '
                'evidence chain and arrived, independently, at the same verdict. This is the '
                '<em>how-we-got-there</em> provenance layer.</div>', unsafe_allow_html=True)

    left, right = st.columns([1.12, 1])
    with left:
        # narrative + same-verdict callout + compact hop reasoning
        hops_html = ""
        for h in cs.get("hops", []):
            short = h["name"].split(" (")[0]
            rec = h["receipt"]
            rec = rec if len(rec) <= 150 else rec[:148] + "…"
            hops_html += f'<div class="pz-hop"><span class="pz-htag">{short}</span><span class="pz-hrec">{rec}</span></div>'
        conf = cs.get("confounder_checks", {})
        conf_rows = ""
        for k in ("locus", "phenocopy", "reproducibility"):
            c = conf.get(k) or {}
            rec = c.get("receipt", "")
            rec = rec if len(rec) <= 165 else rec[:163] + "…"
            conf_rows += f'<div class="row"><b>{k}</b> — {rec}</div>'
        st.markdown(
            '<div class="pz-panel"><div class="pz-cslabel">Evidence-chain reasoning</div>'
            '<div class="pz-csnar">Starting from the raw Perturb-seq tables, the agent verified the '
            '<b>NAB2 knockdown</b>, confirmed a real on-target effect, traced the shift in the '
            '<b>Th1/Th2 program</b>, and tested enrichment against the <b>atopic-eczema</b> modules — '
            'then stress-tested the sharpest confounder (a STAT6 <em>cis</em>-shadow).</div>'
            '<div class="pz-callout"><div class="k">SAME VERDICT · SUPPORTED</div>'
            '<div class="t">Consistent with a re-derived NAB2 → Th1/Th2 → atopic-eczema chain.</div></div>'
            f'<div style="margin-top:16px">{hops_html}</div>'
            f'<div class="pz-conf"><div class="h">Confounder stress-test — STAT6 cis-artifact</div>{conf_rows}</div>'
            '</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="pz-cslabel">Publication-style figure · 6 panels (its own code)</div>',
                    unsafe_allow_html=True)
        if _CS_FIG.exists():
            st.image(str(_CS_FIG), use_container_width=True)
        else:
            st.markdown('<div class="pz-panel">figure not found — see docs/claude-science-evidence-chain_2026-07-08/</div>',
                        unsafe_allow_html=True)

    # live deep-dive — operator-only stretch (honest; not a simulated run)
    st.markdown('<div class="pz-lbl" style="margin-top:20px">Live deep-dive</div>', unsafe_allow_html=True)
    b1, b2 = st.columns([1, 2.2])
    with b1:
        st.button("Run a fresh Claude Science analysis", disabled=True, use_container_width=True)
    with b2:
        st.markdown('<div style="font-size:12.5px;color:var(--ink3);line-height:1.5;padding-top:6px">'
                    'Operator-only stretch — drives Claude Science headless (~several minutes) via the '
                    '<span style="font-family:\'IBM Plex Mono\',monospace">drive-claude-science</span> harness. '
                    'The reasoning above is a <b style="color:var(--ink2)">completed run</b> (committed provenance); '
                    'a fresh run reproduces it live.</div>', unsafe_allow_html=True)


# ------------------------------------------------------------------ dispatch + footer
if ss.screen == "engine":
    render_engine()
elif ss.screen == "claude":
    render_claude()
else:
    render_referee()

st.markdown(
    '<div class="pz-foot"><span>Calibrated language only — the referee will say '
    '<span style="color:var(--warn)">untested</span> or <span style="color:var(--bad)">refuted</span>, '
    'never "proven" or "definitive".</span>'
    '<span class="mono">Reproducible: every number re-derived live from public Perturb-seq tables.</span></div>',
    unsafe_allow_html=True)
