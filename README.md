# 🚀 Startup Metrics Dashboard — Full Portfolio Project

**Author:** Pretty | MCA Final Year  
**Stack:** Python · Streamlit · Plotly · Pandas · SQL · SQLite

---

## 📁 Project Structure

```
startup_metrics/
├── data/
│   ├── users.csv           ← 2,000 simulated users
│   ├── events.csv          ← 16,000+ user events (5 funnel stages)
│   └── sessions.csv        ← Session-level data
│
├── sql/
│   └── startup_metrics_queries.sql  ← 12 production SQL queries
│
├── notebook/
│   └── startup_metrics_analysis.ipynb  ← Full Jupyter analysis
│
├── dashboard/
│   └── app.py              ← Streamlit interactive dashboard
│
├── generate_data.py        ← Script to regenerate dataset
├── requirements.txt        ← Python dependencies
└── README.md               ← This file
```

---

## 📊 Metrics Covered

| Metric | Description |
|--------|-------------|
| **DAU / MAU / WAU** | Daily, Monthly, Weekly Active Users |
| **Stickiness** | DAU ÷ MAU ratio |
| **Day-1 / Day-7 / Day-30 Retention** | Who comes back |
| **Cohort Retention Heatmap** | Month-by-month retention matrix |
| **Conversion Funnel** | Signup → Activation → Feature → Upgrade → Paying |
| **Drop-off Analysis** | Where users leave & why |
| **North Star Metric** | Weekly Active Paying Users (WAPU) |
| **Revenue** | MRR, AOV, Revenue by plan & channel |
| **Channel Performance** | Which acquisition channel converts best |
| **PM Insights** | Auto-generated "What's Going Wrong?" section |

---

## 🛠️ Setup & Run

### Step 1 — Install dependencies
```bash
pip install streamlit plotly pandas numpy
```

### Step 2 — Generate dataset (already done — CSVs included)
```bash
python generate_data.py
```

### Step 3 — Run the dashboard
```bash
cd dashboard
streamlit run app.py
```
Opens at: **http://localhost:8501**

### Step 4 — Open Jupyter Notebook
```bash
pip install jupyter
jupyter notebook notebook/startup_metrics_analysis.ipynb
```

### Step 5 — Run SQL queries
Use any SQLite client (DB Browser for SQLite — free download)  
or run directly in Python:
```python
import sqlite3, pandas as pd
conn = sqlite3.connect(':memory:')
users  = pd.read_csv('data/users.csv')
events = pd.read_csv('data/events.csv')
users.to_sql('users',  conn, index=False)
events.to_sql('events', conn, index=False)
result = pd.read_sql("SELECT * FROM ...", conn)
```

---

## 🎯 Dashboard Features

- **Sidebar filters** — Date range, Channel, Plan, Country (all interactive!)
- **North Star Metric** — WAPU with weekly trend chart
- **6 KPI Cards** — DAU, MAU, Stickiness, Retention, Revenue, AOV
- **4-tab activity charts** — DAU with 7-day rolling avg, MAU, WAU, NSM trend
- **Retention** — Day 1/7/30 bar chart + Cohort heatmap
- **Funnel** — Visual funnel + drop-off horizontal bar chart
- **Revenue** — Monthly MRR + Plan mix donut + Country breakdown
- **PM Insights** — Auto-generated "What's Going Wrong" based on real numbers
- **Business Recommendations** — 5 actionable items for the product team

---

## 📦 Deliverables Checklist

- [x] Cleaned dataset (users.csv, events.csv, sessions.csv)
- [x] SQL queries file (12 production queries)
- [x] Python notebook (11 analysis cells)
- [x] Interactive Streamlit dashboard
- [ ] 2-min walkthrough video ← Record using Loom (free)

---

## 🎥 Video Walkthrough Script (2 min)

**[0:00–0:15]** "Hi, I'm Pretty. I built a Startup Metrics Dashboard to help product and business teams make data-driven decisions."

**[0:15–0:30]** Show the Hero banner and North Star metric. "This is our North Star — Weekly Active Paying Users. It's the one number that captures whether the product is growing."

**[0:30–1:00]** Show DAU/MAU tabs. "Here we track daily and monthly active users. The dotted line is the 7-day rolling average to smooth out noise."

**[1:00–1:20]** Show funnel + drop-off. "The biggest issue is here — Signup to Activation. 28% of users drop off before experiencing any value."

**[1:20–1:40]** Show retention charts. "Day-1 retention is our early signal. If this is below 30%, we have an onboarding problem."

**[1:40–2:00]** Show PM Insights. "Finally, this section auto-generates actionable insights from the data. This is what I'd bring to a product meeting."

---

Built with ❤️ by **Pretty** | MCA Final Year | AI/ML & Full-Stack Developer
