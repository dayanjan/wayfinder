# CS on-screen capture plan — VERIFIED (2026-07-09 de-risk)

Opened all four target CS conversations headless (saved auth) and screenshotted them, to confirm each
beat's receipt is actually on screen and to find the capture mechanics. Result: concrete, de-risked plan
with a few bounded Friday tunings. (Survey shots were in `<scratch>/conv-*.png`, `artifact-b5-receipt.png`.)

## Verified frame URLs (port 8000 — reconfirm Friday)
| Beat | Conversation | Frame URL |
|---|---|---|
| b4 | Live LBD micro-sweep | `http://localhost:8000/projects/proj_64a5e671c715/frames/2b61c815-3e41-48fb-945c-618e8e94a190` |
| b5 | Loose gene-universe sweep | `http://localhost:8000/projects/proj_fd9d7046d730/frames/681b75c5-64eb-48dc-a239-f8a45c1fcb88` |
| b6a | Stage3 STAT6 cis-check | `http://localhost:8000/projects/proj_ea76f1a08006/frames/fb886080-da06-492a-bfec-df1a972955bf` |
| b6b | Stage5 receipt-chain (Reviewer) | `http://localhost:8000/projects/proj_99ccc044f003/frames/4473ddef-0858-47f8-a4f8-408ce5ecfdcf` |

Home→click-by-title also works (all 4 opened) and is the more screen-only "user opens their conversation"
flow; the frame URLs are the robust fallback.

## Per-beat money shot — where it actually is
| Beat | Money shot | Visible on load? | How to capture |
|---|---|---|---|
| **b4** | Ranked table + **"Liveness proof (this run)"** (`ab→7`, `bc→30473`, `ac_lit→82`, OT `MONDO_0004979→3000`) + `executed_code.py` ("from-scratch generator I ran") | ✅ **YES** (bottom view) | Screenshot on load; optional: open `executed_code.py` thumbnail |
| **b6a** | **"Cis-exclusion statement (calibrated)"**: STAT6 unmoved (+0.09/0.79) → cis refuted; NAB2 self −3.08 (z −17) | ✅ **YES** (bottom view) | Screenshot on load |
| **b5** | Funnel + **NAB2 rank** (ab 66 / bc 2184 / ac_lit 6 / ac_known 0.0376 / effect 301 / supported) | ⚠️ in `receipt.md` **artifact** | Open the receipt.md **thumbnail card** (NOT the inline text — inline click only jumps the transcript). Backup: the acceptance-criteria transcript block shows the same NAB2 signals. |
| **b6b** | Reviewer **flags "definitive"/"validated"** (calibrated-language) → edited out | ⚠️ up-transcript / `review.json` | Reach the calibrated-language finding (scroll up or open `review.json`). Bottom view shows only a weaker cosmetic `—` finding. |

## Capture mechanics — SOLVE FRIDAY (bounded)
1. **Conversations open at the BOTTOM** (latest message). b4/b6a money shots happen to be there; b5/b6b need to reach earlier content.
2. **`page.mouse.wheel` does NOT scroll the transcript** (window-level wheel is inert; CS scrolls an inner element). Fixes, in preference order:
   - **Open the receipt artifact** (`receipt.md` / `receipt_chain.md` thumbnail card) → clean, purpose-built receipt view. Best for video.
   - Focus the transcript element then keyboard `Home`/`PageUp`, or `locator.scrollIntoViewIfNeeded()` on a target text node, or element-level `evaluate(el=>el.scrollTop=...)` — but scenes.mjs must stay screen-only (evaluate-scroll belongs in a capture helper, not a demo action).
3. **Artifact thumbnails need a card selector**, not `getByText('receipt.md')` (15 matches; first is inline code). Target the GENERATED thumbnail (e.g. `locator('...thumbnail...:has-text("receipt.md")')` — inspect the DOM Friday).
4. **Dismiss/crop UI chrome**: the "Where you left off / N new" tooltip (top-center) and the persistent "Update available" toast (bottom-right, `f2472dbd → …`). Click their ✕ after load, or crop in post. **Do NOT click "Restart now."**

## Honesty note carried from the shots
- b4 shows **"Review — blocked"** (delegation/ultra-mode off) — the micro-sweep's Reviewer did not run there; the live Reviewer-catches-overclaim moment is the **stage5 (b6b)** conversation. Keep beat 6's "platform checks itself" tied to b6b, not b4.
- b4's liveness proof is the genuine LIVE beat (TADA2B counts re-verified against live Europe PMC). Use it — never imply the full sweep was a live crawl.
