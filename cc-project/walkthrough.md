# CFO Bot — Build Walkthrough

## What Was Built

A fully client-side SPA at [public/index.html](file:///Users/kalybaynurdaulet/Desktop/cc-project/public/index.html) using vanilla JS + Tailwind CDN, deployable via `firebase deploy`.

### Project Structure
```
cc-project/
├── public/
│   └── index.html   ← entire SPA
├── firebase.json    ← Firebase Hosting config
└── Phase 1(specification).docx
```

---

## Key Implementation Decisions

| Decision | Detail |
|---|---|
| **Reactivity** | `oninput` on both number inputs + range sliders; no Calculate button |
| **Sanitization** | `parseInt(...) \|\| 0` + `Math.max(0, ...)` — prevents NaN and negative inputs |
| **Division-by-zero guard** | `C_per_user = (U === 0) ? 0 : C_total / U` |
| **Bandwidth formula** | [(T × 2 / (1024 × 1024)) × 0.12](file:///Users/kalybaynurdaulet/Desktop/cc-project/public/index.html#277-278) — exact KB→GB conversion |
| **Sliders + number inputs** | Bidirectionally synced; sliders cap at 200K users / 500 messages |
| **Cost distribution bar** | Proportional % bar showing how each component contributes to total |
| **Formatting** | `toFixed(2)` for main costs; `toFixed(4)` for bandwidth and per-user |

---

## Math Verification Results (Node.js)

The exact JS formulas from [index.html](file:///Users/kalybaynurdaulet/Desktop/cc-project/public/index.html) were run through a verification script against the 3 approved test cases.

```
=== TC1: Zero Traffic ===  T_msg=0
PASS  Compute      actual=0.000000  expected~0
PASS  DB           actual=0.000000  expected~0
PASS  LLM          actual=0.000000  expected~0
PASS  Bandwidth    actual=0.000000  expected~0
PASS  Total        actual=0.000000  expected~0
PASS  Per User     actual=0.000000  expected~0
PASS  NaN/Inf guard

=== TC2: Standard Load ===  T_msg=500,000
PASS  Compute      actual=0.200000  expected~0.2
PASS  DB           actual=1.500000  expected~1.5
PASS  LLM          actual=97.500000 expected~97.5
PASS  Bandwidth    actual=0.114441  expected~0.1144
PASS  Total        actual=99.314441 expected~99.31
PASS  Per User     actual=0.009931  expected~0.00993
PASS  NaN/Inf guard

=== TC3: High Load ===  T_msg=20,000,000
PASS  Compute      actual=8.000000    expected~8
PASS  DB           actual=60.000000   expected~60
PASS  LLM          actual=3900.000000 expected~3900
PASS  Bandwidth    actual=4.577637    expected~4.5776
PASS  Total        actual=3972.577637 expected~3972.58
PASS  Per User     actual=0.039726    expected~0.0397
PASS  NaN/Inf guard
```

**21 / 21 checks PASSED ✅**

---

## Deploy Command

```bash
cd cc-project
firebase deploy
```
