# CFO Bot — Test Specifications (Phase 1)

> **Purpose:** Guarantee mathematical accuracy of the cost engine.  
> **Method:** Each expected value is manually derived, step-by-step, from the SSOT formulas.  
> **Pass Condition:** UI output must match expected value to ±$0.001 (rounding tolerance only).

---

## Test Case 1: Zero Traffic

**Inputs:** `U = 0`, `M = 0`  
**Purpose:** Validate graceful handling of the zero/empty state (no NaN, no division-by-zero crash).

### Step-by-Step Calculation

| Step | Formula | Calculation | Result |
|---|---|---|---|
| Derived | T_msg = U × M | 0 × 0 | **0** |
| C_compute | T_msg × (0.40 / 1,000,000) | 0 × 0.0000004 | **$0.00** |
| Reads Cost | (T_msg × 2) × (0.06 / 100,000) | 0 | $0.00 |
| Writes Cost | (T_msg × 1) × (0.18 / 100,000) | 0 | $0.00 |
| C_db | Reads + Writes | 0 + 0 | **$0.00** |
| Input Token Cost | (T_msg × 500) × (0.15 / 1,000,000) | 0 | $0.00 |
| Output Token Cost | (T_msg × 200) × (0.60 / 1,000,000) | 0 | $0.00 |
| C_llm | Input + Output | 0 + 0 | **$0.00** |
| C_bandwidth | (T_msg × 2 / 1,048,576) × 0.12 | 0 | **$0.00** |
| C_total | Sum of all above | 0 | **$0.00** |
| C_per_user | U = 0 → return 0 (safe guard) | — | **$0.00** |

### ✅ Expected UI Output

| Field | Expected Value |
|---|---|
| Total Monthly Messages (T_msg) | 0 |
| Compute Cost | $0.00 |
| Database Cost | $0.00 |
| LLM API Cost | $0.00 |
| Bandwidth Cost | $0.0000 |
| **Total Monthly Cost** | **$0.00** |
| **Unit Cost (Per User)** | **$0.0000** |

> [!IMPORTANT]
> The application must **not** throw a `NaN` or `Infinity` error. If U=0 and the code attempts `C_total / U`, it must return `$0.00`, not `Infinity`. This is the primary acceptance criterion for TC1.

---

## Test Case 2: Standard Load

**Inputs:** `U = 10,000`, `M = 50`  
**Purpose:** Validate correct formula execution under realistic, typical SaaS-scale traffic.

### Step-by-Step Calculation

| Step | Formula | Calculation | Result |
|---|---|---|---|
| Derived | T_msg = 10,000 × 50 | | **500,000** |
| **C_compute** | 500,000 × (0.40 / 1,000,000) | 500,000 × 0.0000004 | **$0.20** |
| Reads Cost | (500,000 × 2) × (0.06 / 100,000) | 1,000,000 × 0.0000006 | $0.60 |
| Writes Cost | (500,000 × 1) × (0.18 / 100,000) | 500,000 × 0.0000018 | $0.90 |
| **C_db** | 0.60 + 0.90 | | **$1.50** |
| Input Token Cost | (500,000 × 500) × (0.15 / 1,000,000) | 250,000,000 × 0.00000015 | $37.50 |
| Output Token Cost | (500,000 × 200) × (0.60 / 1,000,000) | 100,000,000 × 0.0000006 | $60.00 |
| **C_llm** | 37.50 + 60.00 | | **$97.50** |
| C_bandwidth | (500,000 × 2 / 1,048,576) × 0.12 | (1,000,000 / 1,048,576) × 0.12 | 0.9537 × 0.12 |
| **C_bandwidth** | | | **$0.1145** |
| **C_total** | 0.20 + 1.50 + 97.50 + 0.1145 | | **$99.31** |
| **C_per_user** | 99.3145 / 10,000 | | **$0.0099** |

### ✅ Expected UI Output

| Field | Expected Value |
|---|---|
| Total Monthly Messages (T_msg) | 500,000 |
| Compute Cost | $0.20 |
| Database Cost | $1.50 |
| LLM API Cost | $97.50 |
| Bandwidth Cost | $0.1145 |
| **Total Monthly Cost** | **$99.31** |
| **Unit Cost (Per User)** | **$0.0099** |

> [!NOTE]
> The LLM API cost ($97.50) dominates — approximately **98%** of total cost. This validates the SSOT's design intent: the calculator should make this trade-off immediately visible to a CFO.

---

## Test Case 3: High Load / Stress Test

**Inputs:** `U = 100,000`, `M = 200`  
**Purpose:** Validate numerical precision and correct scaling at production-grade traffic levels (10× users, 4× messages vs TC2).

### Step-by-Step Calculation

| Step | Formula | Calculation | Result |
|---|---|---|---|
| Derived | T_msg = 100,000 × 200 | | **20,000,000** |
| **C_compute** | 20,000,000 × (0.40 / 1,000,000) | 20,000,000 × 0.0000004 | **$8.00** |
| Reads Cost | (20,000,000 × 2) × (0.06 / 100,000) | 40,000,000 × 0.0000006 | $24.00 |
| Writes Cost | (20,000,000 × 1) × (0.18 / 100,000) | 20,000,000 × 0.0000018 | $36.00 |
| **C_db** | 24.00 + 36.00 | | **$60.00** |
| Input Token Cost | (20,000,000 × 500) × (0.15 / 1,000,000) | 10,000,000,000 × 0.00000015 | $1,500.00 |
| Output Token Cost | (20,000,000 × 200) × (0.60 / 1,000,000) | 4,000,000,000 × 0.0000006 | $2,400.00 |
| **C_llm** | 1,500.00 + 2,400.00 | | **$3,900.00** |
| C_bandwidth | (20,000,000 × 2 / 1,048,576) × 0.12 | (40,000,000 / 1,048,576) × 0.12 | 38.147 × 0.12 |
| **C_bandwidth** | | | **$4.5776** |
| **C_total** | 8.00 + 60.00 + 3,900.00 + 4.5776 | | **$3,972.58** |
| **C_per_user** | 3,972.5776 / 100,000 | | **$0.0397** |

### ✅ Expected UI Output

| Field | Expected Value |
|---|---|
| Total Monthly Messages (T_msg) | 20,000,000 |
| Compute Cost | $8.00 |
| Database Cost | $60.00 |
| LLM API Cost | $3,900.00 |
| Bandwidth Cost | $4.5776 |
| **Total Monthly Cost** | **$3,972.58** |
| **Unit Cost (Per User)** | **$0.0397** |

> [!WARNING]
> At this scale, the LLM cost is **$3,900/month** — roughly 98.2% of total spend. If the calculator returns values significantly different from these, the developer must re-check the token-to-dollar conversion divisor (must use `1,000,000` not `1,000`).

---

## Summary Table — All Test Cases

| Metric | TC1 (U=0, M=0) | TC2 (U=10K, M=50) | TC3 (U=100K, M=200) |
|---|---|---|---|
| T_msg | 0 | 500,000 | 20,000,000 |
| C_compute | $0.00 | $0.20 | $8.00 |
| C_db | $0.00 | $1.50 | $60.00 |
| C_llm | $0.00 | $97.50 | $3,900.00 |
| C_bandwidth | $0.0000 | $0.1145 | $4.5776 |
| **C_total** | **$0.00** | **$99.31** | **$3,972.58** |
| **C_per_user** | **$0.00** | **$0.0099** | **$0.0397** |
