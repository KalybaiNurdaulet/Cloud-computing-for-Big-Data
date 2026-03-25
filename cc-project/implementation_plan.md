# CFO Bot — Implementation Plan (Phase 1)

> **Status:** Approved for Implementation  
> **Stack:** Vanilla HTML · Vanilla JS · Tailwind CSS (CDN) · Firebase Hosting  
> **Constraint:** No frameworks, no build tools, no backend. Pure static SPA.

---

## Overview

Build a single-file, client-side SPA (`public/index.html`) that reads two user inputs (U = Monthly Active Users, M = Messages per User/Month) and instantly re-renders cloud cost breakdowns using the five formulas defined in the SSOT.

---

## Step 1 — Project Scaffold & Firebase Hosting Setup

1. Create the project directory structure:
   ```
   cc-project/
   ├── public/
   │   └── index.html        ← the entire SPA lives here
   └── firebase.json         ← Firebase Hosting config
   ```
2. Create `firebase.json` pointing the `public` directory:
   ```json
   {
     "hosting": {
       "public": "public",
       "ignore": ["firebase.json", "**/.*"]
     }
   }
   ```
3. Run `firebase init hosting` (if not already done) and confirm the above config, then verify with `firebase deploy`.

---

## Step 2 — HTML Skeleton (`public/index.html`)

Create a single `index.html` with:

- **`<head>`**: charset, viewport, title `"CFO Bot — Cloud Cost Calculator"`, Tailwind CDN `<script src="https://cdn.tailwindcss.com"></script>`.
- **`<body>`**: Two-column dashboard layout:
  - **Left panel — Traffic Assumptions (Inputs):**
    - Input field for **U** (Monthly Active Users) — `type="number"`, `min="0"`, `oninput="recalculate()"`, `id="input-users"`
    - Input field for **M** (Avg Messages/User/Month) — same constraints, `id="input-messages"`
    - Display derived variable **T_msg** (read-only, computed)
  - **Right panel — Monthly Cost Breakdown (Outputs):**
    - `id="cost-compute"` — Compute Cost
    - `id="cost-db"` — Database Cost
    - `id="cost-llm"` — LLM API Cost
    - `id="cost-bandwidth"` — Bandwidth Cost
    - `id="cost-total"` — **Total Monthly Cost** (visually prominent)
    - `id="cost-per-user"` — Unit Cost Per User

---

## Step 3 — JavaScript Cost Engine

Implement a single `recalculate()` function (called `oninput`) containing **exactly** the following logic, directly transcribed from the SSOT formulas:

### 3a. Read & Sanitize Inputs
```
U = parseInt(input-users.value) || 0   // never NaN
M = parseInt(input-messages.value) || 0
T_msg = U * M
```

### 3b. Compute Cost (C_compute)
```
C_compute = T_msg * (0.40 / 1_000_000)
```

### 3c. Database Cost (C_db)
```
reads_cost  = (T_msg * 2) * (0.06 / 100_000)
writes_cost = (T_msg * 1) * (0.18 / 100_000)
C_db = reads_cost + writes_cost
```

### 3d. LLM API Cost (C_llm)
```
input_cost  = (T_msg * 500) * (0.15 / 1_000_000)
output_cost = (T_msg * 200) * (0.60 / 1_000_000)
C_llm = input_cost + output_cost
```

### 3e. Bandwidth Cost (C_bandwidth)
```
C_bandwidth = (T_msg * 2 / (1024 * 1024)) * 0.12
```
*(T_msg × 2 KB = total KB; divide by 1,048,576 to get GB; multiply by $0.12)*

### 3f. Total & Unit Economics
```
C_total    = C_compute + C_db + C_llm + C_bandwidth
C_per_user = (U === 0) ? 0 : C_total / U   // safe division
```

### 3g. Render Outputs
- All costs → `toFixed(2)` formatted as `$X.XX`
- `C_per_user` and `C_bandwidth` → `toFixed(4)` at low volumes (display both, or detect low range)
- T_msg → formatted with `.toLocaleString()` for readability

---

## Step 4 — Edge Case Handling

| Scenario | Expected Behavior |
|---|---|
| U = 0, M = 0 | All costs = `$0.00`; Per-User = `$0.00` (no division) |
| U = 0, M > 0 | T_msg = 0; all costs = `$0.00` |
| Negative input | `min="0"` on `<input>` prevents it at the HTML level; JS `||0` fallback prevents NaN |
| Field cleared | `parseInt("")` returns `NaN`; `|| 0` fallback ensures zero |

---

## Step 5 — Styling (Tailwind CSS via CDN)

- Use Tailwind utility classes only — no custom CSS file needed.
- Dark, professional dashboard theme (dark backgrounds, highlighted total row).
- Each cost row: label on left, computed value on right, color-coded (green = low cost, yellow = medium, red = high — optional enhancement).
- Responsive: single-column stack on mobile, two-column side-by-side on `md:` breakpoint.

---

## Step 6 — Deployment

```bash
cd cc-project
firebase deploy
```
Confirm the live URL is accessible and all recalculations work in-browser with zero server calls.

---

## Verification Plan

### Automated (Manual Math Verification)
Run the three canonical test cases defined in `test_specifications.md` against the live app by entering the inputs and validating each output cell matches the pre-calculated expected values to ±$0.01.

### Browser Validation
- Open DevTools Console — zero JS errors on load.
- Confirm `oninput` fires immediately without pressing Enter or a button.
- Confirm clearing both inputs sets all outputs to `$0.00`.
- Confirm negative values are blocked by the `min="0"` HTML attribute.

### Deployment Check
- `firebase deploy` succeeds.
- Live URL loads over HTTPS with no broken resources.
- Tailwind CDN loads (check Network tab — `cdn.tailwindcss.com` returns 200).
