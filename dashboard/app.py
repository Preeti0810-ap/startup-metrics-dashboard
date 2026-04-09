"""
Startup Metrics Dashboard
Author : Preeti | MCA
Stack  : Python · Streamlit · Plotly · Pandas · SQLite
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3, os, random
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(page_title="Startup Metrics", page_icon="🚀",
                   layout="wide", initial_sidebar_state="expanded")

# ═══════════════════════════════════════════════════════════════
# STYLES
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');
*, *::before, *::after { font-family:'Outfit',sans-serif !important; box-sizing:border-box; }

/* Background */
[data-testid="stAppViewContainer"] {
    background:#07091a;
    background-image:
        radial-gradient(ellipse 70% 40% at 15% 5%,  rgba(99,102,241,.14) 0%,transparent 55%),
        radial-gradient(ellipse 55% 35% at 85% 85%, rgba(139,92,246,.11) 0%,transparent 55%),
        radial-gradient(ellipse 40% 30% at 50% 50%, rgba(16,185,129,.04) 0%,transparent 60%);
}
[data-testid="stHeader"]{ background:transparent; }
#MainMenu, footer { visibility:hidden; }
.block-container{ padding:1.5rem 2.5rem !important; max-width:1500px; }

/* Sidebar */
[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#080b1c 0%,#060818 100%) !important;
    border-right:1px solid rgba(99,102,241,.18) !important;
}
[data-testid="stSidebar"] *{ color:#94a3b8 !important; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,[data-testid="stSidebar"] strong{ color:#e2e8f0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label{ color:#94a3b8 !important; }

/* ── Hero ── */
.hero{
    background:linear-gradient(130deg,#0d1225 0%,#111730 60%,#0d1225 100%);
    border:1px solid rgba(99,102,241,.22);
    border-radius:22px; padding:36px 44px; margin-bottom:28px;
    position:relative; overflow:hidden;
}
.hero::before{
    content:''; position:absolute; top:-40%; right:-5%;
    width:450px; height:450px;
    background:radial-gradient(circle,rgba(99,102,241,.09) 0%,transparent 70%);
}
.hero-eyebrow{
    display:inline-flex; align-items:center; gap:6px;
    background:rgba(99,102,241,.13); border:1px solid rgba(99,102,241,.28);
    color:#a5b4fc; border-radius:100px; padding:4px 14px;
    font-size:11px; font-weight:700; letter-spacing:1.5px;
    text-transform:uppercase; margin-bottom:14px;
}
.hero-title{
    font-size:38px; font-weight:800; line-height:1.1; margin:0;
    background:linear-gradient(130deg,#fff 0%,#a5b4fc 55%,#818cf8 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.hero-sub{ color:#475569; font-size:14px; margin-top:10px; }

/* ── Section header ── */
.sh{ display:flex; align-items:center; gap:10px; margin:32px 0 14px; }
.sh-icon{ font-size:20px; }
.sh-title{ color:#e2e8f0; font-size:19px; font-weight:700; margin:0; }
.sh-line{ flex:1; height:1px; background:linear-gradient(90deg,rgba(99,102,241,.3),transparent); }

/* ── KPI Card ── */
.kc{
    background:linear-gradient(145deg,#0d1525,#111d35);
    border:1px solid rgba(255,255,255,.07); border-radius:18px;
    padding:24px 22px; position:relative; overflow:hidden; height:100%;
}
.kc::before{
    content:''; position:absolute; top:0; left:0; right:0; height:2.5px;
    background:var(--ac,linear-gradient(90deg,#6366f1,#8b5cf6));
    border-radius:18px 18px 0 0;
}
.kc-icon{ font-size:26px; display:block; margin-bottom:10px; }
.kc-lbl{ color:#475569; font-size:11px; font-weight:700; letter-spacing:1.4px;
          text-transform:uppercase; margin-bottom:6px; }
.kc-val{ color:#f1f5f9; font-size:32px; font-weight:700;
          font-family:'Space Mono',monospace !important; line-height:1; }
.kc-sub{ font-size:12px; font-weight:600; margin-top:8px;
          padding:3px 10px; border-radius:100px; display:inline-block; }
.green{ background:rgba(16,185,129,.12); color:#34d399; }
.red  { background:rgba(239,68,68,.12);  color:#f87171; }
.blue { background:rgba(99,102,241,.12); color:#a5b4fc; }
.amber{ background:rgba(245,158,11,.12); color:#fbbf24; }

/* ── Chart card ── */
.cc{
    background:linear-gradient(145deg,#0d1525,#111d35);
    border:1px solid rgba(255,255,255,.07); border-radius:18px; padding:22px;
}

/* ── NSM ── */
.nsm{
    background:linear-gradient(135deg,#10102e,#16134a);
    border:1px solid rgba(139,92,246,.35); border-radius:22px;
    padding:44px 28px; text-align:center; position:relative; overflow:hidden;
}
.nsm::after{
    content:'★'; position:absolute; right:16px; top:-16px;
    font-size:110px; opacity:.04; color:#a78bfa; pointer-events:none;
}
.nsm-val{
    font-size:68px; font-weight:800;
    font-family:'Space Mono',monospace !important; line-height:1;
    background:linear-gradient(135deg,#c4b5fd,#818cf8,#6366f1);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.nsm-lbl{
    color:#7c3aed; font-size:11px; font-weight:700;
    letter-spacing:3px; text-transform:uppercase; margin-top:10px;
}
.nsm-desc{ color:#475569; font-size:13px; margin-top:14px; line-height:1.6; }

/* ── Insight row ── */
.ins{
    display:flex; align-items:flex-start; gap:12px;
    background:#0d1525; border:1px solid rgba(255,255,255,.06);
    border-radius:14px; padding:15px 17px; margin:8px 0;
    color:#94a3b8; font-size:14px; line-height:1.6;
}
.ins-ic{ font-size:20px; flex-shrink:0; margin-top:1px; }
.ins b{ color:#e2e8f0; display:block; margin-bottom:3px; }
.ins.ok    { border-left:3px solid #10b981; }
.ins.warn  { border-left:3px solid #f59e0b; }
.ins.danger{ border-left:3px solid #ef4444; }

/* ── Funnel row ── */
.fr{
    display:flex; align-items:center; justify-content:space-between;
    background:#0d1525; border:1px solid rgba(255,255,255,.06);
    border-radius:13px; padding:15px 18px; margin:7px 0;
}
.fr-lbl{ color:#64748b; font-size:11px; font-weight:700;
          letter-spacing:1px; text-transform:uppercase; margin-bottom:3px; }
.fr-val{ color:#f1f5f9; font-size:22px; font-weight:700;
          font-family:'Space Mono',monospace !important; }
.fr-badge{ font-size:12px; font-weight:600; padding:4px 12px;
            border-radius:100px; background:rgba(99,102,241,.15); color:#a5b4fc; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{
    background:#0d1525; border-radius:11px; padding:4px;
    border:1px solid rgba(255,255,255,.06); gap:4px;
}
.stTabs [data-baseweb="tab"]{
    border-radius:8px !important; color:#64748b !important;
    font-weight:600; font-size:13px; padding:6px 16px !important;
}
.stTabs [aria-selected="true"]{
    background:rgba(99,102,241,.2) !important; color:#a5b4fc !important;
}

/* ── Selectbox / slider ── */
[data-baseweb="select"] > div{
    background:#0d1525 !important; border-color:rgba(99,102,241,.3) !important;
    color:#e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# DATA GENERATION (cached)
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def generate_and_load(v=4):  # bump v to clear old cache
    np.random.seed(42); random.seed(42)
    N=2000; DAYS=180; START=datetime(2025,10,1)

    # Users
    rows=[]
    for uid in range(1,N+1):
        sd=START+timedelta(days=random.randint(0,DAYS-1))
        rows.append({"user_id":uid,"signup_date":sd.date(),
            "plan":random.choices(["free","basic","pro","enterprise"],[.6,.2,.15,.05])[0],
            "channel":random.choices(["organic","paid_ad","referral","social","email"],[.35,.25,.20,.12,.08])[0],
            "country":random.choices(["India","USA","UK","Germany","Canada","Australia","Singapore"],[.35,.25,.12,.10,.08,.06,.04])[0],
            "age":random.randint(18,55)})
    users=pd.DataFrame(rows)

    FUNNEL=["signup","activation","feature_use","upgrade","paying"]
    CONV  =[1.0,0.72,0.58,0.35,0.22]
    events=[]
    for _,u in users.iterrows():
        uid=u["user_id"]; sdt=datetime.combine(u["signup_date"],datetime.min.time())
        rem=max(1,DAYS-int((sdt-START).days)-1); n=min(max(1,int(np.random.poisson(4))),rem)
        r=random.random(); ms=max(i for i,c in enumerate(CONV) if r<=c)
        events.append({"user_id":uid,"event":"signup","event_date":sdt.date(),
                        "event_ts":sdt,"revenue":0.0})
        for sc,doff in enumerate(sorted(random.sample(range(rem),n)),1):
            edt=sdt+timedelta(days=doff,hours=random.randint(0,23),minutes=random.randint(0,59))
            for si in range(1,ms+1):
                sn=FUNNEL[si]
                rev=(round(random.choice([9.99,19.99,49.99,99.99]),2) if sn=="paying"
                     else round(random.uniform(5,20),2) if sn=="upgrade" else 0.0)
                events.append({"user_id":uid,"event":sn,"event_date":edt.date(),
                                "event_ts":edt+timedelta(minutes=si*2),"revenue":rev})

    ev=pd.DataFrame(events)
    ev["event_date"]=pd.to_datetime(ev["event_date"])
    ev["event_ts"]  =pd.to_datetime(ev["event_ts"])
    users["signup_date"]=pd.to_datetime(users["signup_date"])
    return users, ev

users_df, events_df = generate_and_load(v=4)

# ═══════════════════════════════════════════════════════════════
# SIDEBAR — Filters
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🚀 Startup Metrics")
    st.markdown("---")

    # Date range
    min_d = events_df["event_date"].min().date()
    max_d = events_df["event_date"].max().date()
    st.markdown("### 📅 Date Range")
    date_from = st.date_input("From", min_d, min_value=min_d)
    date_to   = st.date_input("To",   max_d, min_value=min_d)

    st.markdown("### 🌍 Channel")
    channels = ["All"] + sorted(users_df["channel"].unique().tolist())
    sel_channel = st.selectbox("Acquisition Channel", channels)

    st.markdown("### 💳 Plan")
    plans = ["All"] + sorted(users_df["plan"].unique().tolist())
    sel_plan = st.selectbox("Subscription Plan", plans)

    st.markdown("### 🌐 Country")
    countries = ["All"] + sorted(users_df["country"].unique().tolist())
    sel_country = st.selectbox("Country", countries)

    st.markdown("---")
    st.markdown("""
**📦 Dataset:**
- 2,000 simulated users
- 5 funnel stages
- 90 days of activity

**🔧 Built with:**
Python · Streamlit · Plotly · Pandas
""")

# ═══════════════════════════════════════════════════════════════
# FILTER DATA
# ═══════════════════════════════════════════════════════════════
filtered_users = users_df.copy()
if sel_channel != "All": filtered_users = filtered_users[filtered_users["channel"]==sel_channel]
if sel_plan    != "All": filtered_users = filtered_users[filtered_users["plan"]==sel_plan]
if sel_country != "All": filtered_users = filtered_users[filtered_users["country"]==sel_country]

filtered_ids = set(filtered_users["user_id"])
ev = events_df[
    (events_df["user_id"].isin(filtered_ids)) &
    (events_df["event_date"] >= pd.Timestamp(date_from)) &
    (events_df["event_date"] <= pd.Timestamp(date_to))
].copy()

ev["month"] = ev["event_date"].dt.to_period("M")
ev["week"]  = ev["event_date"].dt.to_period("W")

# ═══════════════════════════════════════════════════════════════
# COMPUTE METRICS
# ═══════════════════════════════════════════════════════════════
# DAU
dau = ev.groupby("event_date")["user_id"].nunique().reset_index()
dau.columns = ["date","dau"]

# MAU
mau = ev.groupby("month")["user_id"].nunique().reset_index()
mau.columns = ["month","mau"]; mau["ms"]=mau["month"].astype(str)

# WAU
wau = ev.groupby("week")["user_id"].nunique().reset_index()
wau.columns = ["week","wau"]; wau["ws"]=wau["week"].astype(str)

# NSM — weekly paying users
nsm = ev[ev["event"]=="paying"].groupby("week")["user_id"].nunique().reset_index()
nsm.columns=["week","wpau"]; nsm["ws"]=nsm["week"].astype(str)

latest_mau   = int(mau["mau"].iloc[-1]) if len(mau) else 0
dau_avg      = int(dau["dau"].tail(30).mean()) if len(dau) else 0
stickiness   = round(dau_avg/latest_mau*100,1) if latest_mau else 0

# Funnel
fun  = ev.groupby("event")["user_id"].nunique()
f_signup  = fun.get("signup",0)
f_activ   = fun.get("activation",0)
f_feat    = fun.get("feature_use",0)
f_upgrade = fun.get("upgrade",0)
f_paying  = fun.get("paying",0)

def pct(a,b): return round(a/b*100,1) if b else 0

# Retention Day 1/7/30
signup_dates = ev[ev["event"]=="signup"].groupby("user_id")["event_date"].min().rename("signup_date")
activity     = ev.groupby("user_id")["event_date"].apply(set)
def check_ret(uid, sd, days):
    if uid not in activity.index: return 0
    return int(any((d-sd).days in range(days, days+2) for d in activity[uid]))

ret_df = signup_dates.reset_index()
ret_df["d1"]  = ret_df.apply(lambda r: check_ret(r.user_id, r.signup_date,  1), axis=1)
ret_df["d7"]  = ret_df.apply(lambda r: check_ret(r.user_id, r.signup_date,  7), axis=1)
ret_df["d30"] = ret_df.apply(lambda r: check_ret(r.user_id, r.signup_date, 30), axis=1)
n_total = len(ret_df)
d1_ret  = pct(ret_df["d1"].sum(),  n_total)
d7_ret  = pct(ret_df["d7"].sum(),  n_total)
d30_ret = pct(ret_df["d30"].sum(), n_total)

# Revenue
rev_total  = round(ev[ev["event"]=="paying"]["revenue"].sum(), 2)
rev_monthly= ev[ev["event"]=="paying"].groupby("month")["revenue"].sum().reset_index()
rev_monthly.columns=["month","revenue"]; rev_monthly["ms"]=rev_monthly["month"].astype(str)
aov = round(rev_total/f_paying,2) if f_paying else 0

# Cohort retention heatmap — use month_num (int) to avoid Period NaT crash entirely
ev["month_num"] = ev["event_date"].dt.year * 12 + ev["event_date"].dt.month
ev["ym_str"]    = ev["event_date"].dt.strftime("%Y-%m")

cohort_num = ev[ev["event"]=="signup"].groupby("user_id")["month_num"].min().rename("cohort_num")
cohort_str = ev[ev["event"]=="signup"].groupby("user_id")["ym_str"].min().rename("cohort_str")

ev3 = ev[["user_id","month_num","ym_str"]].drop_duplicates()
ev3 = ev3.join(cohort_num, on="user_id").join(cohort_str, on="user_id")
ev3 = ev3.dropna(subset=["cohort_num"])
ev3["cohort_num"] = ev3["cohort_num"].astype(int)
ev3["period"]     = (ev3["month_num"] - ev3["cohort_num"]).astype(int)

coh       = ev3.groupby(["cohort_str","period"])["user_id"].nunique().reset_index()
coh_pivot = coh.pivot(index="cohort_str", columns="period", values="user_id")
first_col  = coh_pivot.columns[0]
coh_ret    = (coh_pivot.divide(coh_pivot[first_col], axis=0) * 100).round(1).fillna(0)

# Channel performance
ch_perf = filtered_users.copy()
paying_ids = set(ev[ev["event"]=="paying"]["user_id"])
ch_perf["converted"] = ch_perf["user_id"].isin(paying_ids).astype(int)
ch_agg = ch_perf.groupby("channel").agg(signups=("user_id","count"), paying=("converted","sum")).reset_index()
ch_agg["conv_pct"] = (ch_agg["paying"]/ch_agg["signups"]*100).round(1)

# Drop-off table
drop = pd.DataFrame({
    "Stage": ["Signup → Activation","Activation → Feature Use","Feature Use → Upgrade","Upgrade → Paying"],
    "Drop %": [pct(f_signup-f_activ,f_signup), pct(f_activ-f_feat,f_activ),
                pct(f_feat-f_upgrade,f_feat),  pct(f_upgrade-f_paying,f_upgrade)]
})

# ═══════════════════════════════════════════════════════════════
# CHART THEME
# ═══════════════════════════════════════════════════════════════
CT = dict(
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Outfit", color="#64748b", size=12),
    xaxis=dict(gridcolor="rgba(255,255,255,.04)", linecolor="rgba(255,255,255,.06)",
               tickfont=dict(color="#475569")),
    yaxis=dict(gridcolor="rgba(255,255,255,.04)", linecolor="rgba(255,255,255,.06)",
               tickfont=dict(color="#475569")),
    margin=dict(l=10,r=10,t=20,b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#64748b")),
)

def chart(fig, h=300):
    fig.update_layout(**CT, height=h)
    return fig

# ═══════════════════════════════════════════════════════════════
# ── HERO ────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
h1, h2 = st.columns([3,1])
with h1:
    st.markdown(f"""
    <div class="hero">
        <div class="hero-eyebrow">🚀 Live Dashboard</div>
        <div class="hero-title">Startup Metrics Dashboard</div>
        <div class="hero-sub">
            {len(filtered_users):,} users &nbsp;·&nbsp; {len(ev):,} events &nbsp;·&nbsp;
            {str(date_from)} → {str(date_to)} &nbsp;·&nbsp;
            Channel: <b style="color:#a5b4fc">{sel_channel}</b> &nbsp;·&nbsp;
            Plan: <b style="color:#a5b4fc">{sel_plan}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
with h2:
    st.markdown("<br>", unsafe_allow_html=True)
    if sel_channel!="All" or sel_plan!="All" or sel_country!="All":
        st.info("🔍 Filters active — data is scoped")
    else:
        st.success("✅ Showing all data")

# ═══════════════════════════════════════════════════════════════
# ── NORTH STAR ──────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="sh"><span class="sh-icon">⭐</span><span class="sh-title">North Star Metric</span><div class="sh-line"></div></div>', unsafe_allow_html=True)

n1, n2, n3 = st.columns([1,2,1])
with n2:
    latest_wpau = int(nsm["wpau"].iloc[-1]) if len(nsm) else 0
    st.markdown(f"""
    <div class="nsm">
        <div class="nsm-val">{latest_wpau:,}</div>
        <div class="nsm-lbl">Weekly Active Paying Users (WAPU)</div>
        <div class="nsm-desc">
            The one metric that best represents product growth.<br>
            Users who pay = users who found real value.<br>
            <strong style="color:#a78bfa">Target: grow this 10% week-over-week.</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# ── KPI CARDS ───────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="sh"><span class="sh-icon">📊</span><span class="sh-title">Key Performance Indicators</span><div class="sh-line"></div></div>', unsafe_allow_html=True)

c1,c2,c3,c4,c5,c6 = st.columns(6)

def kpi_card(col, icon, label, value, sub, cls, accent="linear-gradient(90deg,#6366f1,#8b5cf6)"):
    col.markdown(f"""
    <div class="kc" style="--ac:{accent}">
        <span class="kc-icon">{icon}</span>
        <div class="kc-lbl">{label}</div>
        <div class="kc-val">{value}</div>
        <div class="kc-sub {cls}">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

kpi_card(c1,"👥","Avg DAU",  f"{dau_avg:,}", "Last 30 days","blue")
kpi_card(c2,"📅","Latest MAU",f"{latest_mau:,}","Monthly users","blue","linear-gradient(90deg,#8b5cf6,#a78bfa)")
kpi_card(c3,"🔥","Stickiness",f"{stickiness}%","DAU÷MAU",
         "green" if stickiness>20 else "amber","linear-gradient(90deg,#10b981,#34d399)" if stickiness>20 else "linear-gradient(90deg,#f59e0b,#fbbf24)")
kpi_card(c4,"🔁","Day-1 Ret.", f"{d1_ret}%","Return next day",
         "green" if d1_ret>30 else "red","linear-gradient(90deg,#10b981,#34d399)" if d1_ret>30 else "linear-gradient(90deg,#ef4444,#f87171)")
kpi_card(c5,"💰","Total Rev.",  f"${rev_total:,.0f}","All time","green","linear-gradient(90deg,#10b981,#059669)")
kpi_card(c6,"🧾","Avg Order",  f"${aov}","Per paying user","blue","linear-gradient(90deg,#6366f1,#4f46e5)")

# ═══════════════════════════════════════════════════════════════
# ── DAU / MAU / WAU ─────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="sh"><span class="sh-icon">📅</span><span class="sh-title">User Activity Over Time</span><div class="sh-line"></div></div>', unsafe_allow_html=True)

t1,t2,t3,t4 = st.tabs(["📈 Daily Active Users","📊 Monthly Active Users","📉 Weekly Active Users","⭐ NSM Trend"])

with t1:
    fig = px.area(dau, x="date", y="dau", color_discrete_sequence=["#6366f1"])
    fig.update_traces(fill="tozeroy", fillcolor="rgba(99,102,241,0.1)", line_width=2.5)
    # 7-day rolling avg
    dau["rolling7"] = dau["dau"].rolling(7).mean()
    fig.add_scatter(x=dau["date"], y=dau["rolling7"], mode="lines",
                    name="7-day avg", line=dict(color="#f59e0b", width=2, dash="dot"))
    st.plotly_chart(chart(fig, 320), use_container_width=True)

with t2:
    fig = px.bar(mau, x="ms", y="mau", color_discrete_sequence=["#8b5cf6"],
                 labels={"ms":"Month","mau":"MAU"})
    fig.update_traces(marker_cornerradius=6)
    st.plotly_chart(chart(fig, 320), use_container_width=True)

with t3:
    fig = px.line(wau, x="ws", y="wau", color_discrete_sequence=["#a78bfa"],
                  labels={"ws":"Week","wau":"WAU"}, markers=True)
    fig.update_traces(line_width=2.5, marker_size=7)
    st.plotly_chart(chart(fig, 320), use_container_width=True)

with t4:
    if len(nsm):
        fig = go.Figure()
        fig.add_bar(x=nsm["ws"], y=nsm["wpau"], name="WAPU",
                    marker_color="rgba(99,102,241,0.4)")
        fig.add_scatter(x=nsm["ws"], y=nsm["wpau"], mode="lines+markers",
                        name="Trend", line=dict(color="#a78bfa", width=2.5), marker_size=6)
        st.plotly_chart(chart(fig, 320), use_container_width=True)
    else:
        st.info("No paying users in selected filters.")

# ═══════════════════════════════════════════════════════════════
# ── RETENTION ───────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="sh"><span class="sh-icon">🔁</span><span class="sh-title">Retention Analysis</span><div class="sh-line"></div></div>', unsafe_allow_html=True)

ra, rb = st.columns([1,2])

with ra:
    # Day 1/7/30 gauge-style
    ret_data = pd.DataFrame({
        "Period": ["Day 1","Day 7","Day 30"],
        "Retention %": [d1_ret, d7_ret, d30_ret],
        "Color": ["#6366f1","#8b5cf6","#a78bfa"]
    })
    fig = go.Figure()
    for _, row in ret_data.iterrows():
        fig.add_trace(go.Bar(
            x=[row["Period"]], y=[row["Retention %"]],
            marker_color=row["Color"], name=row["Period"],
            text=[f"{row['Retention %']}%"], textposition="outside",
            textfont=dict(color="#e2e8f0", size=14, family="Space Mono")
        ))
    fig.update_layout(**CT, height=300, showlegend=False)
    fig.update_yaxes(range=[0, max(d1_ret, d7_ret, d30_ret)*1.3+5])
    st.plotly_chart(fig, use_container_width=True)

with rb:
    # Cohort heatmap
    if not coh_ret.empty and coh_ret.shape[1] > 1:
        display = coh_ret.iloc[:, :6]
        fig = px.imshow(display,
            labels=dict(x="Month After Signup", y="Cohort", color="Ret %"),
            color_continuous_scale=[[0,"#080c1e"],[0.25,"#1e1b4b"],[0.6,"#4338ca"],[1,"#a5b4fc"]],
            text_auto=".0f", aspect="auto")
        fig.update_layout(**CT, height=300,
            coloraxis_colorbar=dict(title="Ret%",tickfont=dict(color="#475569"),title_font=dict(color="#475569")))
        fig.update_traces(textfont_size=11)
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# ── CONVERSION FUNNEL ───────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="sh"><span class="sh-icon">🌀</span><span class="sh-title">Conversion Funnel & Drop-off</span><div class="sh-line"></div></div>', unsafe_allow_html=True)

fa, fb, fc = st.columns([2,1,1])

with fa:
    stages = ["Signup","Activation","Feature Use","Upgrade","Paying"]
    vals   = [f_signup, f_activ, f_feat, f_upgrade, f_paying]
    colors = ["#6366f1","#7c3aed","#8b5cf6","#a78bfa","#10b981"]
    fig = go.Figure(go.Funnel(
        y=stages, x=vals,
        textposition="inside", textinfo="value+percent initial",
        marker=dict(color=colors, line=dict(color=["#4338ca","#5b21b6","#6d28d9","#7c3aed","#059669"],width=2)),
        connector=dict(line=dict(color="rgba(255,255,255,.05)",width=1))
    ))
    st.plotly_chart(chart(fig, 360), use_container_width=True)

with fb:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="fr"><div><div class="fr-lbl">Signup → Activation</div><div class="fr-val">{pct(f_activ,f_signup)}%</div></div>
    <span class="fr-badge">{"✅" if pct(f_activ,f_signup)>65 else "⚠️"}</span></div>
    <div class="fr"><div><div class="fr-lbl">Activation → Feature</div><div class="fr-val">{pct(f_feat,f_activ)}%</div></div>
    <span class="fr-badge">{"✅" if pct(f_feat,f_activ)>70 else "⚠️"}</span></div>
    <div class="fr"><div><div class="fr-lbl">Feature → Upgrade</div><div class="fr-val">{pct(f_upgrade,f_feat)}%</div></div>
    <span class="fr-badge">{"✅" if pct(f_upgrade,f_feat)>50 else "⚠️"}</span></div>
    <div class="fr"><div><div class="fr-lbl">Upgrade → Paying</div><div class="fr-val">{pct(f_paying,f_upgrade)}%</div></div>
    <span class="fr-badge">{"✅" if pct(f_paying,f_upgrade)>55 else "⚠️"}</span></div>
    """, unsafe_allow_html=True)

with fc:
    st.markdown("<br>", unsafe_allow_html=True)
    # Drop-off bar
    fig = px.bar(drop, x="Drop %", y="Stage", orientation="h",
                 color="Drop %", color_continuous_scale=["#10b981","#f59e0b","#ef4444"],
                 labels={"Drop %":"Drop-off %"})
    fig.update_layout(**CT, height=320, showlegend=False, coloraxis_showscale=False)
    fig.update_xaxes(range=[0, 100])
    fig.update_traces(marker_cornerradius=4)
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# ── REVENUE & CHANNELS ──────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="sh"><span class="sh-icon">💰</span><span class="sh-title">Revenue & Acquisition Channels</span><div class="sh-line"></div></div>', unsafe_allow_html=True)

re1, re2 = st.columns([3,2])

with re1:
    if len(rev_monthly):
        fig = px.bar(rev_monthly, x="ms", y="revenue", color_discrete_sequence=["#10b981"],
                     labels={"ms":"Month","revenue":"Revenue ($)"})
        fig.update_traces(marker_cornerradius=6)
        st.plotly_chart(chart(fig, 300), use_container_width=True)

with re2:
    fig = px.bar(ch_agg.sort_values("conv_pct",ascending=True),
                 x="conv_pct", y="channel", orientation="h",
                 color="conv_pct", color_continuous_scale=["#1e1b4b","#6366f1","#a5b4fc"],
                 labels={"conv_pct":"Conversion %","channel":"Channel"})
    fig.update_traces(marker_cornerradius=4)
    fig.update_layout(**CT, height=300, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# Plan mix donut
pl1, pl2 = st.columns(2)
with pl1:
    plan_mix = filtered_users.groupby("plan")["user_id"].count().reset_index()
    plan_mix.columns=["plan","count"]
    fig = px.pie(plan_mix, names="plan", values="count", hole=0.55,
                 color_discrete_sequence=["#6366f1","#8b5cf6","#10b981","#f59e0b"])
    fig.update_layout(**CT, height=280, title=dict(text="Plan Mix",font=dict(color="#94a3b8",size=14)))
    fig.update_traces(textfont_color="#e2e8f0")
    st.plotly_chart(fig, use_container_width=True)

with pl2:
    country_mix = filtered_users.groupby("country")["user_id"].count().reset_index()
    country_mix.columns=["country","count"]
    fig = px.bar(country_mix.sort_values("count",ascending=False),
                 x="country", y="count", color_discrete_sequence=["#8b5cf6"],
                 labels={"country":"Country","count":"Users"})
    fig.update_traces(marker_cornerradius=5)
    fig.update_layout(**CT, height=280, title=dict(text="Users by Country",font=dict(color="#94a3b8",size=14)))
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# ── WHAT'S GOING WRONG ──────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="sh"><span class="sh-icon">🔥</span><span class="sh-title">What\'s Going Wrong? (PM Insights)</span><div class="sh-line"></div></div>', unsafe_allow_html=True)

issues, goods = [], []

activation_rate = pct(f_activ, f_signup)
if activation_rate < 60:
    issues.append(("danger","🔴","Low Activation Rate",
        f"Only {activation_rate}% of signups activate. Fix your onboarding — users aren't seeing value fast enough. Try a product tour or 'aha moment' trigger within first 5 minutes."))
if d1_ret < 25:
    issues.append(("danger","🔴","Poor Day-1 Retention",
        f"{d1_ret}% of users return on Day 1. This is your biggest leak. Add a welcome email sequence, push notification, or 'next step' CTA immediately after signup."))
if d7_ret < 15:
    issues.append(("warn","🟡","Weak Week-1 Retention",
        f"Day-7 retention is {d7_ret}%. Users aren't forming a habit. Introduce a weekly digest, streak feature, or re-engagement campaign at Day 3 and Day 5."))
if pct(f_upgrade,f_feat) < 50:
    issues.append(("warn","🟡","Feature → Upgrade Drop-off",
        f"Only {pct(f_upgrade,f_feat)}% of active users upgrade. Consider a 'paywall moment' — show upgrade benefits right when a user tries a premium feature."))
if stickiness < 15:
    issues.append(("warn","🟡","Low Stickiness",
        f"DAU/MAU = {stickiness}%. Users aren't making this a daily habit. Add a daily value loop — notifications, daily digest, or gamification."))

# Positives
if activation_rate >= 65: goods.append(("ok","🟢","Strong Activation",f"{activation_rate}% activation rate — your onboarding is working well."))
if d1_ret >= 30:          goods.append(("ok","🟢","Good Day-1 Retention",f"{d1_ret}% users return on Day 1 — strong initial engagement."))
if stickiness >= 20:      goods.append(("ok","🟢","Healthy Stickiness",f"{stickiness}% DAU/MAU — users are forming a daily habit."))
if pct(f_paying,f_signup)>= 20: goods.append(("ok","🟢","Solid Conversion to Paid",f"{pct(f_paying,f_signup)}% of signups become paying users."))

if not issues: issues.append(("ok","🟢","All Clear","No critical issues detected in the selected filters. Focus on scaling what's working."))

col_ins1, col_ins2 = st.columns(2)
all_issues = issues + goods
for i, (cls,icon,title,msg) in enumerate(all_issues):
    col = col_ins1 if i%2==0 else col_ins2
    col.markdown(f'<div class="ins {cls}"><span class="ins-ic">{icon}</span><div><b>{title}</b>{msg}</div></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# ── BUSINESS RECOMMENDATIONS ────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="sh"><span class="sh-icon">📋</span><span class="sh-title">Business Recommendations</span><div class="sh-line"></div></div>', unsafe_allow_html=True)

recs = [
    ("🎯","Fix Onboarding First",
     "The biggest drop-off is Signup → Activation. This means users sign up but don't experience value. Priority #1: redesign the onboarding to deliver the 'aha moment' within 3 minutes of signup."),
    ("📧","Launch a Retention Email Sequence",
     "Day-1 and Day-7 retention are below benchmarks. A 5-email drip sequence (Welcome, Tips, Case Study, Feature Highlight, Upgrade Offer) can lift retention by 15-25%."),
    ("💎","Double Down on Referral Channel",
     f"Referral users likely have the highest LTV. If referral conversion is high in your data, invest in a referral program — offer both referrer and referee a free month."),
    ("📊","Track North Star Weekly",
     "Make WAPU (Weekly Active Paying Users) your team's one metric. Every product decision should answer: 'Does this grow WAPU?'"),
    ("🔒","Introduce a Smart Paywall",
     f"Only {pct(f_paying,f_signup)}% of signups convert to paid. Show the upgrade prompt at the exact moment a user tries a premium feature — contextual paywalls convert 3x better than blanket prompts."),
]

for i in range(0, len(recs), 2):
    cols = st.columns(2)
    for j, col in enumerate(cols):
        if i+j < len(recs):
            icon, title, body = recs[i+j]
            col.markdown(f"""
            <div class="ins ok" style="border-left-color:#6366f1;align-items:flex-start">
                <span class="ins-ic">{icon}</span>
                <div><b>{title}</b>{body}</div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#1e293b;font-size:13px;
border-top:1px solid rgba(255,255,255,.05);padding-top:20px;">
    Built by <strong style="color:#6366f1">Pretty</strong> &nbsp;·&nbsp;
    MCA Final Year &nbsp;·&nbsp;
    Python · Streamlit · Plotly · Pandas · SQL &nbsp;·&nbsp;
    🚀 Startup Metrics Dashboard
</div>
""", unsafe_allow_html=True)
