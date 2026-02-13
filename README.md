# nil-causal-impact
"Do NIL Collectives Actually Improve Collegiate Athletic Performance?"
Framework
Step 1: Collect Data
Team-level performance metrics (wins, rankings, times)
NIL collective formation dates by school
Recruiting rankings before and after NIL
Conference fixed effects
Budget data (if available)

Scrape sports-reference
Use NCAA data
Pull 247Sports recruiting rankings
Track NIL formation year manually


Step 2: Methodology
Difference-in-Differences (DiD)
Fixed effects regression
Event study design
Robustness checks
Parallel trends validation
Model:
Performanceit=α+βNILit+γi+δt+ϵit

Step 3: Output
Publication-quality visualizations
Statistical significance tables
Sensitivity analyses
Policy interpretation

What’s Not Been Done (Yet)
Key gaps in current work are:
Causal analysis of NIL or NIL collectives on actual in-game performance outcomes
Few, if any, peer-reviewed papers currently measure performance metrics (wins, points differential, recruiting success, team rankings) as a function of NIL effects.
Quantitative econometric studies focusing on individual/team performance rather than finance or identity
Some early econometric work exists for revenue but not performance — your proposed DiD or panel analysis on performance would be novel.
Studies that explicitly model the role of NIL collectives (as opposed to NIL overall)
Collectives are distinct from NIL deals themselves — they pool resources and potentially influence recruiting in ways not captured by most current research.

---

# Tech Stack 

### Primary Stack

* **Python**
* `pandas` (panel construction)
* `statsmodels` (econometrics, fixed effects, DiD)
* `linearmodels` (PanelOLS — very clean for FE models)
* `numpy`
* `matplotlib` / `seaborn`
* `scipy`
* Optional: `econml`

---

# Data Architecture

## Final Target Dataset Structure


| team | year | wins | srs | recruiting_rank | nil_collective | nil_year | conference | ... |
| ---- | ---- | ---- | --- | --------------- | -------------- | -------- | ---------- | --- |

Where each row is:

> (team, year)

This becomes a **panel dataset**.

---

# Raw Data Files

### Team Performance Data

One CSV:

`team_performance.csv`

Columns:

* team
* year
* wins
* losses
* win_pct
* points_for
* points_against
* srs (if available)
* conference

Years: ideally 2015–2025 (gives good pre/post NIL window)

---

### Recruiting Data

One CSV:

`recruiting_rankings.csv`

Columns:

* team
* year
* recruiting_rank
* avg_star_rating
* total_recruit_score

Source: 247Sports composite rankings

---

### NIL / Collective Data

One CSV:

`nil_data.csv`

Columns:

* team
* collective_exists (0/1)
* collective_start_year
* estimated_collective_strength (optional)
* state_nillaw_year (optional)


```
treatment_it = 1 if year >= collective_start_year
```

This enables:

* Difference-in-Differences with staggered treatment
* Event study design
* More credible causal inference

---

# Important Identification Challenge

NIL became legal nationally in 2021.

So the challenge is:

> How do we isolate collective effects from national NIL policy shock?

Possible strategies:

### Use variation in collective formation timing

Not all schools formed collectives immediately.

### Use variation in collective intensity

Some are much larger and better funded.

### Use state NIL laws pre-2021

Some states passed laws earlier.

---

# Workflow

### Phase 1: Build Clean Panel Dataset

* Merge performance + recruiting + NIL
* Create treatment indicators
* Create time dummies
* Encode conference fixed effects

---

### Phase 2: Baseline DiD Model

[
Performance_{it} = \alpha + \beta Treatment_{it} + \gamma_i + \delta_t + \epsilon_{it}
]

Where:

* ( \gamma_i ) = team fixed effects
* ( \delta_t ) = year fixed effects

This controls for:

* Team quality
* National trends
* COVID
* Transfer portal era

---

### Phase 3: Event Study

Create:

```
years_since_collective = year - collective_start_year
```

Then estimate dynamic treatment effects.

Plot coefficients.

This shows:

* Parallel trends pre-treatment
* Treatment effect trajectory

---

# Outcomes?

Best primary outcomes:

* Win percentage
* SRS (Simple Rating System)
* Recruiting rank (secondary outcome)
* Points differential

NOT only wins — too noisy.

---

# Data Size

134 teams × ~10 years = 1,340 rows.

Even with recruiting classes:

~2,000–3,000 rows total.
