import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_generator import generate_all_data, generate_district_summary, generate_sport_summary, SPORTS, DISTRICTS
from datetime import datetime
import os, base64, glob, time
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Notun Kuri - National Talent Stipend Program", page_icon="\U0001F1E7\U0001F1E9", layout="wide", initial_sidebar_state="expanded")

GREEN = "#006A4E"
RED = "#F42A41"
GOLD = "#D4AF37"

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
.stApp { font-family: 'Inter', sans-serif; }
.hero { background: linear-gradient(135deg, #006A4E 0%, #004D3C 40%, #1A1A2E 100%); padding: 2.5rem 3rem; border-radius: 16px; margin-bottom: 2rem; position: relative; overflow: hidden; }
.hero::before { content: ''; position: absolute; top: -50%; right: -20%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(244,42,65,0.15) 0%, transparent 70%); border-radius: 50%; }
.hero h1 { color: white; margin: 0; font-size: 2rem; font-weight: 800; position: relative; z-index: 1; }
.hero p { color: #B0D4C8; margin: 0.4rem 0 0; font-size: 1rem; position: relative; z-index: 1; }
.hero .badge-row { margin-top: 1rem; position: relative; z-index: 1; }
.hero .hero-badge { display: inline-block; padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin-right: 0.5rem; background: rgba(255,255,255,0.15); color: white; }
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
.kpi-card { background: white; padding: 1.2rem 1.5rem; border-radius: 12px; box-shadow: 0 1px 6px rgba(0,0,0,0.06); border-top: 3px solid #006A4E; }
.kpi-card .kpi-value { font-size: 1.8rem; font-weight: 800; color: #1A1A2E; margin: 0; }
.kpi-card .kpi-label { font-size: 0.8rem; color: #6C757D; margin: 0.3rem 0 0; }
.kpi-card .kpi-delta { font-size: 0.75rem; margin: 0.2rem 0 0; }
.kpi-card .kpi-delta.up { color: #198754; }
.kpi-card .kpi-delta.down { color: #DC3545; }
.section-title { font-size: 1.1rem; font-weight: 700; color: #1A1A2E; margin: 1.5rem 0 0.8rem; padding-bottom: 0.5rem; border-bottom: 2px solid #006A4E; }
.insight-card { background: linear-gradient(135deg, #F0F8FF 0%, #E8F4FD 100%); padding: 1.2rem 1.5rem; border-radius: 12px; border-left: 4px solid #0D6EFD; margin: 0.5rem 0; }
.insight-card.warning { background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); border-left-color: #F59E0B; }
.insight-card.danger { background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%); border-left-color: #EF4444; }
.insight-card.success { background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%); border-left-color: #22C55E; }
.profile-header { background: linear-gradient(135deg, #006A4E 0%, #1A1A2E 100%); padding: 2rem; border-radius: 16px; color: white; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 2rem; }
.profile-avatar { width: 80px; height: 80px; border-radius: 50%; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 800; border: 3px solid rgba(255,255,255,0.3); }
.profile-info h2 { margin: 0; font-size: 1.5rem; font-weight: 700; }
.profile-info p { margin: 0.2rem 0; color: #B0D4C8; font-size: 0.9rem; }
.tier-badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
.tier-top { background: #D4EDDA; color: #155724; }
.tier-pipeline { background: #FFF3CD; color: #856404; }
.report-header { background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%); padding: 2rem; border-radius: 16px; color: white; margin-bottom: 1.5rem; border: 1px solid rgba(255,255,255,0.1); }
.report-header h2 { margin: 0; font-size: 1.4rem; color: white; }
.report-header p { margin: 0.3rem 0 0; color: #94A3B8; font-size: 0.9rem; }
</style>""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_data():
    df = generate_all_data()
    return df, generate_district_summary(df), generate_sport_summary(df)

df, district_summary, sport_summary = load_data()
sport_list = list(SPORTS.keys())
district_list = sorted(DISTRICTS.keys())

def header(title, subtitle, badges=None):
    badge_html = ""
    if badges:
        badge_html = '<div class="badge-row">' + "".join(f'<span class="hero-badge">{b}</span>' for b in badges) + "</div>"
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p>{badge_html}</div>', unsafe_allow_html=True)

def kpi_row(items):
    html = '<div class="kpi-grid">'
    for val, label, delta, direction in items:
        d = "up" if direction == "up" else "down"
        dh = f'<p class="kpi-delta {d}">{delta}</p>' if delta else ""
        html += f'<div class="kpi-card"><p class="kpi-value">{val}</p><p class="kpi-label">{label}</p>{dh}</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

PL = dict(font=dict(family="Inter, sans-serif", size=12), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=40, b=20))

def banner_carousel(skip_first=False):
    banner_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "banners")
    exts = ("*.png","*.jpg","*.jpeg","*.webp","*.gif")
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(banner_dir, ext)))
    files = sorted(files)
    if skip_first and files:
        files = files[1:]
    if not files:
        st.markdown("""<div style="background:linear-gradient(135deg,#006A4E 0%,#004D3C 40%,#1A1A2E 100%); padding:3rem; border-radius:16px; text-align:center;">
            <p style="color:#B0D4C8; font-size:0.95rem; margin:0;">Place banner images in the <code>banners/</code> folder</p>
            <p style="color:#6C757D; font-size:0.8rem; margin:0.5rem 0 0;">Supported: png / jpg / jpeg / webp / gif</p>
        </div>""", unsafe_allow_html=True)
        return
    n = len(files)
    state_key = "banner_idx"
    if state_key not in st.session_state:
        st.session_state[state_key] = 0
    idx = st.session_state[state_key] % n

    st.markdown("""<style>
    div[data-testid="stImage"] { margin-top: -1rem; }
    div[data-testid="stImage"] + div[data-testid="stHorizontalBlock"] {
        margin-top: -36px; position: relative; z-index: 10; text-align: center;
    }
    div[data-testid="stImage"] + div[data-testid="stHorizontalBlock"] div[data-testid="column"] {
        padding: 0 !important; margin: 0 !important; width: auto !important;
        display: flex !important; justify-content: center !important; align-items: center !important;
    }
    div[data-testid="stImage"] + div[data-testid="stHorizontalBlock"] div[data-testid="column"] button[kind="secondary"] {
        width: 10px !important; height: 10px !important; min-width: 10px !important; min-height: 10px !important;
        border-radius: 50% !important; padding: 0 !important; border: none !important;
        background: rgba(255,255,255,0.4) !important; color: transparent !important;
        font-size: 0 !important; line-height: 0 !important;
        box-shadow: 0 0 4px rgba(0,0,0,0.3) !important; transition: all 0.2s !important;
    }
    div[data-testid="stImage"] + div[data-testid="stHorizontalBlock"] div[data-testid="column"] button[kind="secondary"]:hover {
        background: rgba(255,255,255,0.85) !important;
    }
    </style>""", unsafe_allow_html=True)

    from PIL import Image
    _first = Image.open(files[0])
    _tw, _th = _first.size
    _target_h = _th - 50
    _img = Image.open(files[idx])
    _ratio = _tw / _img.width
    _new_h = int(_img.height * _ratio)
    _img = _img.resize((_tw, _new_h), Image.LANCZOS)
    if _new_h > _target_h:
        _img = _img.crop((0, 0, _tw, _target_h))
    elif _new_h < _target_h:
        _padded = Image.new(_img.mode, (_tw, _target_h), (0, 0, 0))
        _padded.paste(_img, (0, 0))
        _img = _padded
    _scale = 2 / 3
    _img = _img.resize((int(_tw * _scale), int(_target_h * _scale)), Image.LANCZOS)
    st.image(_img, use_container_width=True)

    _pad = 4
    dot_cols = st.columns([_pad] + [1]*n + [_pad])
    for i in range(n):
        with dot_cols[i + 1]:
            if st.button(" ", key=f"bdot_{i}"):
                st.session_state[state_key] = i
                st.rerun()

# SIDEBAR
with st.sidebar:
    st.markdown(f"""<div style="text-align:center; padding:1rem 0;">
        <img src="https://flagcdn.com/w80/bd.png" alt="Bangladesh Flag" style="width:64px; height:auto; border-radius:4px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        <h3 style="margin:0.5rem 0 0; color:#006A4E; font-weight:800;">Notun Kuri</h3>
        <p style="margin:0; color:#6C757D; font-size:0.8rem;">National Talent Stipend Program</p>
        <p style="margin:0.2rem 0 0; color:#ADB5BD; font-size:0.7rem;">Ministry of Sports & Youth Affairs</p>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["\U0001F4CA  Overview", "\U0001F4CA  Dashboard", "\U0001F464  Player Directory", "\U0001F3AF  Player Profile", "\U0001F9E0  AI Insights", "\u2694\uFE0F  Head-to-Head", "\U0001F504  Promotion & Relegation", "\U0001F5FA  District Analytics", "\U0001F3C6  Sport Analytics", "\U0001F4CB  Ministry Reports"], index=0, label_visibility="collapsed")
    st.markdown("---")
    top_n = (df["Tier"] == "TOP").sum()
    pipe_n = (df["Tier"] == "PIPELINE").sum()
    tb = df["Stipend (BDT)"].sum()
    st.markdown(f"""<div style="background:#F8F9FA; padding:1rem; border-radius:10px;">
        <p style="margin:0; font-size:0.75rem; color:#6C757D; font-weight:600;">PROGRAM OVERVIEW</p>
        <div style="display:flex; justify-content:space-between; margin-top:0.5rem;">
            <div><span style="font-size:1.2rem; font-weight:800; color:#006A4E;">{top_n}</span><br><span style="font-size:0.7rem; color:#6C757D;">Top Tier</span></div>
            <div><span style="font-size:1.2rem; font-weight:800; color:#FFC107;">{pipe_n}</span><br><span style="font-size:0.7rem; color:#6C757D;">Pipeline</span></div>
            <div><span style="font-size:1.2rem; font-weight:800; color:#0D6EFD;">{len(df)}</span><br><span style="font-size:0.7rem; color:#6C757D;">Total</span></div>
        </div>
        <hr style="margin:0.8rem 0; border:none; border-top:1px solid #DEE2E6;">
        <p style="margin:0; font-size:0.75rem; color:#6C757D;">Monthly Budget</p>
        <p style="margin:0; font-size:1.1rem; font-weight:700; color:#1A1A2E;">&#2547; {tb:,.0f}</p>
    </div>""", unsafe_allow_html=True)

# ============ OVERVIEW ============
if page == "\U0001F4CA  Overview":
    banner_carousel()
    st.divider()
    top_df = df[df["Tier"] == "TOP"]
    pipe_df = df[df["Tier"] == "PIPELINE"]
    kpi_row([("800", "Total Athletes", "+200 from last cohort", "up"), ("400", "Top Tier (Stipend)", "Active recipients", "up"), ("400", "Pipeline Tier", "Candidates", "up"), (f"{df['Overall Rating'].mean():.1f}", "Avg Rating", f"+{df['Performance Trend'].mean():.1f} trend", "up"), (f"{df['Total Medals'].sum()}", "Total Medals", f"{df['Gold Medals'].sum()} gold", "up"), (f"\u09F3{df['Stipend (BDT)'].sum():,.0f}", "Monthly Budget", "Govt funded", "up")])
    c1, c2, c3 = st.columns(3)
    with c1:
        gc = df["Gender"].value_counts()
        fig = px.pie(values=gc.values, names=gc.index, title="Gender Split", color_discrete_map={"Male": GREEN, "Female": RED}, hole=0.45)
        fig.update_traces(textinfo="label+value+percent"); fig.update_layout(**PL, height=320); st.plotly_chart(fig, use_container_width=True)
    with c2:
        sc = df["Primary Sport"].value_counts()
        fig = px.pie(values=sc.values, names=sc.index, title="Sports Distribution", color_discrete_sequence=px.colors.qualitative.Set3, hole=0.45)
        fig.update_traces(textinfo="percent+label", textfont_size=9); fig.update_layout(**PL, height=320); st.plotly_chart(fig, use_container_width=True)
    with c3:
        tc = df["Tier"].value_counts()
        fig = px.pie(values=tc.values, names=tc.index, title="Tier Split", color_discrete_map={"TOP": GREEN, "PIPELINE": GOLD}, hole=0.45)
        fig.update_traces(textinfo="label+value+percent"); fig.update_layout(**PL, height=320); st.plotly_chart(fig, use_container_width=True)

    banner_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "banners")
    _bf = []
    for _ext in ("*.png","*.jpg","*.jpeg","*.webp","*.gif"):
        _bf.extend(glob.glob(os.path.join(banner_dir, _ext)))
    _bf = sorted(_bf)
    if len(_bf) > 1:
        time.sleep(4)
        st.session_state["banner_idx"] = (st.session_state.get("banner_idx", 0) + 1) % len(_bf)
        st.rerun()

# ============ DASHBOARD ============
if page == "\U0001F4CA  Dashboard":
    header("Notun Kuri Program Dashboard", "Real-time overview of Bangladesh's premier youth talent development initiative", [f"As of {datetime.now().strftime('%B %d, %Y')}", "800 Athletes", "10 Sports", "20 Districts"])
    top_df = df[df["Tier"] == "TOP"]
    kpi_row([("800", "Total Athletes", "+200 from last cohort", "up"), ("400", "Top Tier (Stipend)", "Active recipients", "up"), (f"\u09F3{df['Stipend (BDT)'].sum():,.0f}", "Monthly Budget", "Govt funded", "up"), (f"{df['Overall Rating'].mean():.1f}", "Avg Rating", f"+{df['Performance Trend'].mean():.1f} trend", "up"), (f"{df['Total Medals'].sum()}", "Total Medals", f"{df['Gold Medals'].sum()} gold", "up"), (f"{df['Attendance %'].mean():.1f}%", "Avg Attendance", "Target: 85%", "up")])
    t1, t2, t3, t4 = st.tabs(["\U0001F3C6 Sports", "\u2642\uFE0F\u2640\uFE0F Demographics", "\U0001F5FA Districts", "\U0001F4C8 Trends"])
    with t1:
        c1, c2 = st.columns([2, 1])
        with c1:
            fig = px.bar(sport_summary, x="Sport", y="Athletes", color="Sport", title="Athletes by Sport", text="Athletes", color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(showlegend=False, xaxis_tickangle=-45, **PL); st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.pie(sport_summary, values="Athletes", names="Sport", title="Distribution", color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(textposition="inside", textinfo="percent+label", textfont_size=10); fig.update_layout(**PL, height=380); st.plotly_chart(fig, use_container_width=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Male", x=sport_summary["Sport"], y=sport_summary["Male"], marker_color=GREEN, text=sport_summary["Male"], textposition="outside"))
        fig2.add_trace(go.Bar(name="Female", x=sport_summary["Sport"], y=sport_summary["Female"], marker_color=RED, text=sport_summary["Female"], textposition="outside"))
        fig2.update_layout(barmode="group", title="Gender by Sport", xaxis_tickangle=-45, **PL); st.plotly_chart(fig2, use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(sport_summary.sort_values("Total Medals", ascending=True), x="Total Medals", y="Sport", orientation="h", title="Medals by Sport", color="Total Medals", color_continuous_scale="YlOrRd")
            fig.update_layout(**PL, height=400); st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.scatter(sport_summary, x="Avg Rating", y="Athletes", size="Total Medals", color="Sport", hover_name="Sport", title="Rating vs Participation vs Medals", color_discrete_sequence=px.colors.qualitative.Set3, size_max=40)
            fig.update_layout(**PL, height=400); st.plotly_chart(fig, use_container_width=True)
    with t2:
        c1, c2, c3 = st.columns(3)
        with c1:
            gc = df["Gender"].value_counts()
            fig = px.pie(values=gc.values, names=gc.index, title="Gender Split", color_discrete_map={"Male": GREEN, "Female": RED}, hole=0.4)
            fig.update_traces(textinfo="label+value+percent"); st.plotly_chart(fig, use_container_width=True)
        with c2:
            ac = df["Age"].value_counts().sort_index()
            fig = px.bar(x=ac.index.astype(str), y=ac.values, title="Age Distribution", labels={"x": "Age", "y": "Count"}, color_discrete_sequence=[GREEN], text=ac.values)
            st.plotly_chart(fig, use_container_width=True)
        with c3:
            ag = df.groupby(["Age", "Gender"]).size().reset_index(name="Count")
            fig = px.bar(ag, x="Age", y="Count", color="Gender", barmode="group", title="Age-Gender", color_discrete_map={"Male": GREEN, "Female": RED})
            st.plotly_chart(fig, use_container_width=True)
    with t3:
        c1, c2 = st.columns([3, 2])
        with c1:
            fig = px.bar(district_summary.sort_values("Avg_Rating", ascending=True), x="Avg_Rating", y="District", orientation="h", title="District Rankings", color="Avg_Rating", color_continuous_scale="RdYlGn", range_color=[55, 80], text="Avg_Rating")
            fig.update_layout(**PL, height=600); st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.scatter(district_summary, x="Top_Tier", y="Avg_Rating", size="Total_Athletes", hover_name="District", text="District", title="Top Tier vs Avg Rating", color="Avg_Rating", color_continuous_scale="RdYlGn", size_max=30)
            fig.update_traces(textposition="top center", textfont_size=9); fig.update_layout(**PL, height=600); st.plotly_chart(fig, use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(district_summary.sort_values("Total_Medals", ascending=False).head(12), x="District", y=["Gold", "Silver", "Bronze"], title="Top 12 - Medal Tally", barmode="stack", color_discrete_map={"Gold": "#FFD700", "Silver": "#C0C0C0", "Bronze": "#CD7F32"})
            fig.update_layout(**PL, xaxis_tickangle=-45); st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.bar(district_summary.sort_values("Total_Stipend", ascending=False).head(12), x="District", y="Total_Stipend", title="Top 12 - Stipend", color="Total_Stipend", color_continuous_scale="Greens", text="Total_Stipend")
            fig.update_layout(**PL, xaxis_tickangle=-45); fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside"); st.plotly_chart(fig, use_container_width=True)
    with t4:
        ml = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        np.random.seed(42); td = []
        for sp in sport_list:
            base = df[f"Rating - {sp}"].mean()
            for i, m in enumerate(ml):
                td.append({"Month": m, "Sport": sp, "Avg Rating": round(base + np.sin(i/2)*3 + np.random.normal(0, 1.5), 1)})
        fig = px.line(pd.DataFrame(td), x="Month", y="Avg Rating", color="Sport", title="Monthly Trends", markers=True, color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(**PL); st.plotly_chart(fig, use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(df, x="Performance Trend", nbins=30, title="Trend Distribution", color_discrete_sequence=[GREEN], opacity=0.8)
            fig.add_vline(x=0, line_dash="dash", line_color="red", line_width=1); fig.update_layout(**PL); st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.scatter(df, x="Consistency Score", y="Overall Rating", color="Tier", size="Training Hours/Week", opacity=0.7, title="Consistency vs Rating", color_discrete_map={"TOP": GREEN, "PIPELINE": GOLD}, size_max=15)
            fig.update_layout(**PL); st.plotly_chart(fig, use_container_width=True)

# ============ PLAYER DIRECTORY ============
elif page == "\U0001F464  Player Directory":
    header("Player Directory", "Complete registry of all Notun Kuri athletes", [f"{len(df)} Athletes"])
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: tier_f = st.selectbox("Tier", ["All", "TOP", "PIPELINE"])
    with c2: sport_f = st.selectbox("Sport", ["All"] + sport_list)
    with c3: gender_f = st.selectbox("Gender", ["All", "Male", "Female"])
    with c4: district_f = st.selectbox("District", ["All"] + district_list)
    with c5: age_f = st.selectbox("Age", ["All"] + list(range(8, 15)))
    with c6: status_f = st.selectbox("Status", ["All", "Active", "Recovering"])
    flt = df.copy()
    if tier_f != "All": flt = flt[flt["Tier"] == tier_f]
    if sport_f != "All": flt = flt[flt["Primary Sport"] == sport_f]
    if gender_f != "All": flt = flt[flt["Gender"] == gender_f]
    if district_f != "All": flt = flt[flt["District"] == district_f]
    if age_f != "All": flt = flt[flt["Age"] == age_f]
    if status_f != "All": flt = flt[flt["Status"] == status_f]
    section(f"Results \u2014 {len(flt)} athletes found")
    c1, c2 = st.columns([2, 1])
    with c1: sort_col = st.selectbox("Sort by", ["Overall Rating", "Primary Rating", "Total Medals", "Performance Trend", "Training Hours/Week", "Attendance %", "Age"])
    with c2: sort_dir = st.radio("Order", ["Descending", "Ascending"], horizontal=True)
    flt = flt.sort_values(sort_col, ascending=(sort_dir == "Ascending"))
    display_cols = ["Player ID", "Name", "Gender", "Age", "District", "Primary Sport", "Skill Specialization", "Tier", "Overall Rating", "Primary Rating", "Total Medals", "Gold Medals", "Training Hours/Week", "Attendance %", "Performance Trend", "Stipend (BDT)", "Status"]
    st.dataframe(flt[display_cols], use_container_width=True, height=520)
    c1, c2, c3 = st.columns(3)
    with c1: st.download_button("Download CSV", flt.to_csv(index=False), "notun_kuri_filtered.csv", "text/csv", use_container_width=True)
    with c2: st.download_button("Download Top 400", df[df["Tier"]=="TOP"].to_csv(index=False), "top400.csv", "text/csv", use_container_width=True)
    with c3: st.download_button("Download Pipeline 400", df[df["Tier"]=="PIPELINE"].to_csv(index=False), "pipeline400.csv", "text/csv", use_container_width=True)

# ============ PLAYER PROFILE ============
elif page == "\U0001F3AF  Player Profile":
    header("Player Profile", "Detailed athlete analytics and performance intelligence")
    names_list = [f"{r['Player ID']}  |  {r['Name']}  |  {r['Primary Sport']}" for _, r in df.iterrows()]
    selected = st.selectbox("Select Athlete", names_list)
    pid = selected.split("|")[0].strip()
    p = df[df["Player ID"] == pid].iloc[0]
    tc = "tier-top" if p["Tier"] == "TOP" else "tier-pipeline"
    st.markdown(f"""<div class="profile-header">
        <div class="profile-avatar">{p['Name'][0]}</div>
        <div class="profile-info">
            <h2>{p['Name']} <span class="tier-badge {tc}">{p['Tier']}</span></h2>
            <p>{p['Player ID']} \u2022 {p['Gender']} \u2022 Age {p['Age']} \u2022 {p['District']}</p>
            <p>{p['Primary Sport']} ({p['Skill Specialization']}) \u2022 {p['Training Center']}</p>
        </div>
    </div>""", unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Overall Rating", f"{p['Overall Rating']}")
    c2.metric("Primary Rating", f"{p['Primary Rating']}")
    c3.metric("Total Medals", f"{p['Total Medals']}", f"\U0001F947{p['Gold Medals']} \U0001F948{p['Silver Medals']} \U0001F949{p['Bronze Medals']}")
    c4.metric("Tournaments", f"{p['Tournaments Played']}", f"{p['Win Rate']}% win")
    c5.metric("Training", f"{p['Training Hours/Week']} hrs/wk", f"{p['Attendance %']}% att.")
    ti = "\U0001F4C8" if p["Performance Trend"] > 0 else "\U0001F4C9"
    c6.metric("Trend", f"{p['Performance Trend']:+.1f}", f"{ti} 12-month")
    cl, cr = st.columns(2)
    with cl:
        section("Gauge - Overall Performance")
        fig = go.Figure(go.Indicator(mode="gauge+number+delta", value=p["Overall Rating"], delta=dict(reference=75, increasing=dict(color=GREEN), decreasing=dict(color=RED)),
            gauge=dict(axis=dict(range=[30, 100], dtick=10), bar=dict(color=GREEN, thickness=0.3),
                steps=[dict(range=[30, 55], color="#FEE2E2"), dict(range=[55, 70], color="#FEF3C7"), dict(range=[70, 85], color="#DCFCE7"), dict(range=[85, 100], color="#BBF7D0")],
                threshold=dict(line=dict(color="red", width=3), thickness=0.8, value=75)),
            title=dict(text="Performance Score", font=dict(size=16))))
        fig.update_layout(height=300, **PL); st.plotly_chart(fig, use_container_width=True)
    with cr:
        section("Radar - Multi-Sport Proficiency")
        ratings = {s: p[f"Rating - {s}"] for s in sport_list}
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=list(ratings.values())+[list(ratings.values())[0]], theta=list(ratings.keys())+[list(ratings.keys())[0]], fill="toself", name=p["Name"], fillcolor="rgba(0,106,78,0.25)", line=dict(color=GREEN, width=2), marker=dict(size=6)))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[30, 100])), height=320, showlegend=False, margin=dict(l=60, r=60, t=30, b=30))
        st.plotly_chart(fig, use_container_width=True)
    section("Performance History (12 Months)")
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=p["Performance History"], mode="lines+markers", name="Rating", line=dict(color=GREEN, width=3), marker=dict(size=8, color=GREEN), fill="tozeroy", fillcolor="rgba(0,106,78,0.08)"))
    fig.add_hline(y=75, line_dash="dash", line_color="gray", line_width=1, annotation_text="Top Tier Threshold", annotation_position="top right")
    fig.update_layout(title=f"{p['Name']} - 12 Month Performance", xaxis_title="Month", yaxis_title="Rating", yaxis=dict(range=[30, 100]), height=320, **PL)
    st.plotly_chart(fig, use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        section("Sport-by-Sport Ratings")
        sdf = pd.DataFrame({"Sport": sport_list, "Rating": [ratings[s] for s in sport_list]}).sort_values("Rating", ascending=True)
        colors = [GREEN if r >= 75 else (GOLD if r >= 60 else RED) for r in sdf["Rating"]]
        fig = go.Figure(go.Bar(x=sdf["Rating"], y=sdf["Sport"], orientation="h", marker_color=colors, text=sdf["Rating"], textposition="outside"))
        fig.update_layout(height=400, **PL, xaxis=dict(range=[0, 105])); st.plotly_chart(fig, use_container_width=True)
    with c2:
        section("Profile Details")
        st.markdown(f"| Field | Value |\n|-------|-------|\n| **DOB** | {p['Date of Birth']} |\n| **Region** | {p['Region']} |\n| **Secondary Sport** | {p['Secondary Sport']} |\n| **Stipend** | \u09F3 {p['Stipend (BDT)']:,.0f}/month |\n| **Status** | {p['Status']} |\n| **Peak/Low Rating** | {p['Peak Rating']} / {p['Lowest Rating']} |\n| **Hot Streak** | {p['Hot Streak']} days |\n| **Injuries** | {p['Injury Count']} |\n| **Consistency** | {p['Consistency Score']:.2f} |")
        if p["Tier"] == "TOP":
            r = p["Relegation Risk"]
            if r >= 0.4: st.error(f"Relegation Risk: HIGH ({r*100:.0f}%)")
            elif r >= 0.2: st.warning(f"Relegation Risk: MODERATE ({r*100:.0f}%)")
            else: st.success(f"Relegation Risk: LOW ({r*100:.0f}%)")
        else:
            c = p["Promotion Chance"]
            if c >= 0.6: st.success(f"Promotion Chance: HIGH ({c*100:.0f}%)")
            elif c >= 0.3: st.warning(f"Promotion Chance: MODERATE ({c*100:.0f}%)")
            else: st.error(f"Promotion Chance: LOW ({c*100:.0f}%)")
        st.info(f"Coach: *{p['Coach Remarks']}*")
    section("Tournament History")
    tl = p["Tournament Log"]
    if tl:
        tdf = pd.DataFrame(tl)
        fig = px.bar(tdf, x="event", y="placement", color="placement", color_continuous_scale="RdYlGn_r", range_color=[1, 8], title="Placements (lower = better)", labels={"event": "Tournament", "placement": "Position"})
        fig.update_layout(**PL, xaxis_tickangle=-45); st.plotly_chart(fig, use_container_width=True)
    else: st.info("No tournament history.")

# ============ AI INSIGHTS ============
elif page == "\U0001F9E0  AI Insights":
    header("AI-Powered Intelligence", "Predictive analytics and program optimization insights", ["Machine Learning", "Risk Assessment", "Performance Prediction"])
    top_df = df[df["Tier"] == "TOP"]
    pipe_df = df[df["Tier"] == "PIPELINE"]
    hs = (top_df["Overall Rating"].mean()/100*25 + top_df["Attendance %"].mean()/100*20 + (1-top_df["Relegation Risk"].mean())*20 + min(top_df["Tournaments Won"].sum()/40,1)*15 + (1-(top_df["Status"]=="Recovering").mean())*10 + min(top_df["Total Medals"].sum()/500,1)*10)*100
    kpi_row([(f"{hs:.0f}/100", "Program Health", "\U0001F4C8 +3 vs last quarter", "up"), (f"{df['Performance Trend'].mean():+.2f}", "Avg Trend", "Positive", "up"), (f"{(df['Status']=='Recovering').mean()*100:.1f}%", "Injury Rate", "Target: <5%", "down" if (df['Status']=='Recovering').mean()*100>5 else "up"), (f"{len(top_df[top_df['Relegation Risk']>=0.4])}", "High Relegation Risk", "Needs action", "down"), (f"{len(pipe_df[pipe_df['Promotion Chance']>=0.6])}", "Strong Promotion", "Ready for top", "up"), (f"{df['Total Medals'].sum()}", "Total Medals", f"{df['Gold Medals'].sum()} gold", "up")])
    t1, t2, t3, t4 = st.tabs(["\u26A0\uFE0F Risk Analysis", "\U0001F31F Opportunity Finder", "\U0001F52E Predictions", "\U0001F4DD Recommendations"])
    with t1:
        section("Relegation Risk Analysis")
        rdf = top_df[["Player ID","Name","Primary Sport","Age","District","Overall Rating","Relegation Risk","Performance Trend","Attendance %"]].sort_values("Relegation Risk", ascending=False)
        rdf["Risk Level"] = rdf["Relegation Risk"].apply(lambda x: "HIGH" if x>=0.4 else ("MODERATE" if x>=0.2 else "LOW"))
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(rdf, x="Relegation Risk", nbins=25, title="Risk Distribution", color="Risk Level", color_discrete_map={"HIGH": RED, "MODERATE": "#FFC107", "LOW": GREEN})
            fig.update_layout(**PL); st.plotly_chart(fig, use_container_width=True)
        with c2:
            sr = rdf.groupby("Primary Sport")["Relegation Risk"].mean().sort_values(ascending=True)
            fig = go.Figure(go.Bar(x=sr.values, y=sr.index, orientation="h", marker_color=[RED if v>=0.3 else ("#FFC107" if v>=0.2 else GREEN) for v in sr.values], text=[f"{v*100:.1f}%" for v in sr.values], textposition="outside"))
            fig.update_layout(title="Avg Risk by Sport", **PL); st.plotly_chart(fig, use_container_width=True)
        section("Top 20 High Risk Players")
        st.dataframe(rdf.head(20), use_container_width=True)
    with t2:
        section("Promotion Opportunity Finder")
        odf = pipe_df[["Player ID","Name","Primary Sport","Age","District","Overall Rating","Promotion Chance","Performance Trend","Total Medals"]].sort_values("Promotion Chance", ascending=False)
        odf["Level"] = odf["Promotion Chance"].apply(lambda x: "STRONG" if x>=0.6 else ("MODERATE" if x>=0.3 else "WEAK"))
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(odf, x="Promotion Chance", nbins=25, title="Promotion Distribution", color="Level", color_discrete_map={"STRONG": GREEN, "MODERATE": "#FFC107", "WEAK": RED})
            fig.update_layout(**PL); st.plotly_chart(fig, use_container_width=True)
        with c2:
            sp = odf.groupby("Primary Sport")["Promotion Chance"].mean().sort_values(ascending=True)
            fig = go.Figure(go.Bar(x=sp.values, y=sp.index, orientation="h", marker_color=[GREEN if v>=0.4 else ("#FFC107" if v>=0.25 else RED) for v in sp.values], text=[f"{v*100:.1f}%" for v in sp.values], textposition="outside"))
            fig.update_layout(title="Avg Promotion by Sport", **PL); st.plotly_chart(fig, use_container_width=True)
        section("Top 20 Promotion Candidates")
        st.dataframe(odf.head(20), use_container_width=True)
    with t3:
        section("Performance Predictions")
        c1, c2 = st.columns(2)
        with c1:
            section("\U0001F4C8 Rising Stars")
            st.dataframe(df.nlargest(20, "Performance Trend")[["Player ID","Name","Tier","Primary Sport","Overall Rating","Performance Trend","Consistency Score"]], use_container_width=True)
        with c2:
            section("\U0001F4C9 Declining Performance")
            st.dataframe(df.nsmallest(20, "Performance Trend")[["Player ID","Name","Tier","Primary Sport","Overall Rating","Performance Trend","Consistency Score"]], use_container_width=True)
        section("Most Consistent Performers")
        st.dataframe(df.nsmallest(20, "Consistency Score")[["Player ID","Name","Tier","Primary Sport","Overall Rating","Consistency Score","Performance Trend"]], use_container_width=True)
    with t4:
        section("AI-Generated Recommendations")
        avg_train = df["Training Hours/Week"].mean()
        inj_rate = (df["Status"]=="Recovering").mean()*100
        avg_att = df["Attendance %"].mean()
        recs = []
        if avg_train < 22: recs.append(("warning", "Training Gap", f"Avg training ({avg_train:.1f} hrs/wk) below 22 hr target. Increase structured sessions."))
        if inj_rate > 5: recs.append(("danger", "Injury Concern", f"Injury rate ({inj_rate:.1f}%) above 5% threshold. Review load and recovery."))
        if avg_att < 85: recs.append(("warning", "Attendance", f"Avg attendance ({avg_att:.1f}%) below 85% target."))
        sg = df.groupby("Primary Sport")["Overall Rating"].mean()
        recs.append(("success", "Sport Strength", f"Strongest: {sg.idxmax()} ({sg.max():.1f}). Weakest: {sg.idxmin()} ({sg.min():.1f})."))
        hr = len(top_df[top_df["Relegation Risk"]>=0.4])
        if hr > 0: recs.append(("danger", "Relegation Alert", f"{hr} athletes at high relegation risk. Deploy targeted coaching."))
        sp2 = len(pipe_df[pipe_df["Promotion Chance"]>=0.6])
        if sp2 > 0: recs.append(("success", "Promotion Ready", f"{sp2} pipeline athletes ready for promotion."))
        icons = {"warning": "\u26A0\uFE0F", "danger": "\U0001F534", "success": "\u2705", "info": "\u2139\uFE0F"}
        for i, (rt, title, text) in enumerate(recs, 1):
            st.markdown(f'<div class="insight-card {rt}"><strong>{icons.get(rt,"")} {i}. {title}</strong><br>{text}</div>', unsafe_allow_html=True)

# ============ HEAD-TO-HEAD ============
elif page == "\u2694\uFE0F  Head-to-Head":
    header("Player Comparison", "Side-by-side athletic performance analysis")
    names_list = [f"{r['Player ID']}  |  {r['Name']}  |  {r['Primary Sport']}" for _, r in df.iterrows()]
    c1, c2 = st.columns(2)
    with c1:
        p1_sel = st.selectbox("Athlete 1", names_list, key="h1")
        p1 = df[df["Player ID"]==p1_sel.split("|")[0].strip()].iloc[0]
    with c2:
        p2_sel = st.selectbox("Athlete 2", names_list, index=min(40,len(names_list)-1), key="h2")
        p2 = df[df["Player ID"]==p2_sel.split("|")[0].strip()].iloc[0]
    t1c = "tier-top" if p1["Tier"]=="TOP" else "tier-pipeline"
    t2c = "tier-top" if p2["Tier"]=="TOP" else "tier-pipeline"
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="profile-header" style="padding:1.5rem;"><div class="profile-avatar" style="width:60px;height:60px;font-size:1.5rem;">{p1["Name"][0]}</div><div class="profile-info"><h2 style="font-size:1.2rem;">{p1["Name"]} <span class="tier-badge {t1c}">{p1["Tier"]}</span></h2><p>{p1["Primary Sport"]} \u2022 Age {p1["Age"]} \u2022 {p1["District"]}</p></div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="profile-header" style="padding:1.5rem; background:linear-gradient(135deg,#F42A41 0%,#C62828 100%);"><div class="profile-avatar" style="width:60px;height:60px;font-size:1.5rem;">{p2["Name"][0]}</div><div class="profile-info"><h2 style="font-size:1.2rem;">{p2["Name"]} <span class="tier-badge {t2c}">{p2["Tier"]}</span></h2><p>{p2["Primary Sport"]} \u2022 Age {p2["Age"]} \u2022 {p2["District"]}</p></div></div>', unsafe_allow_html=True)
    section("Radar Comparison")
    r1 = [p1[f"Rating - {s}"] for s in sport_list]+[p1[f"Rating - {sport_list[0]}"]]
    r2 = [p2[f"Rating - {s}"] for s in sport_list]+[p2[f"Rating - {sport_list[0]}"]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=r1, theta=sport_list+[sport_list[0]], fill="toself", name=p1["Name"], fillcolor="rgba(0,106,78,0.2)", line=dict(color=GREEN, width=2)))
    fig.add_trace(go.Scatterpolar(r=r2, theta=sport_list+[sport_list[0]], fill="toself", name=p2["Name"], fillcolor="rgba(244,42,65,0.2)", line=dict(color=RED, width=2)))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[30, 100])), height=420, showlegend=True, legend=dict(x=0.5, xanchor="center", y=-0.1, orientation="h"), margin=dict(l=60,r=60,t=30,b=60))
    st.plotly_chart(fig, use_container_width=True)
    section("Metric Comparison")
    cms = ["Overall Rating","Primary Rating","Training Hours/Week","Attendance %","Performance Trend","Consistency Score","Tournaments Played","Tournaments Won","Gold Medals","Silver Medals","Bronze Medals","Total Medals","Win Rate","Hot Streak"]
    cdf = pd.DataFrame({"Metric": cms, p1["Name"]: [p1[m] for m in cms], p2["Name"]: [p2[m] for m in cms]})
    cdf["Leader"] = cdf.apply(lambda row: p1["Name"] if row[p1["Name"]]>row[p2["Name"]] else (p2["Name"] if row[p2["Name"]]>row[p1["Name"]] else "Tie"), axis=1)
    fig = go.Figure()
    fig.add_trace(go.Bar(name=p1["Name"], x=cdf["Metric"], y=cdf[p1["Name"]], marker_color=GREEN))
    fig.add_trace(go.Bar(name=p2["Name"], x=cdf["Metric"], y=cdf[p2["Name"]], marker_color=RED))
    fig.update_layout(barmode="group", xaxis_tickangle=-45, height=400, **PL)
    st.plotly_chart(fig, use_container_width=True)
    p1w = sum(1 for m in cms if p1[m]>p2[m]); p2w = sum(1 for m in cms if p2[m]>p1[m]); ties = len(cms)-p1w-p2w
    kpi_row([(str(p1w), f"{p1['Name']} Leads", "", "up"), (str(ties), "Tied", "", "up"), (str(p2w), f"{p2['Name']} Leads", "", "up")])
    st.dataframe(cdf, use_container_width=True)

# ============ PROMOTION & RELEGATION ============
elif page == "\U0001F504  Promotion & Relegation":
    header("Promotion & Relegation Tracker", "Tier movement management and pipeline readiness", ["Dynamic Tier System", "400 Top + 400 Pipeline"])
    t1, t2, t3 = st.tabs(["\U0001F4CA Current Status", "\U0001F504 Simulator", "\U0001F4CA Threshold Analysis"])
    with t1:
        c1, c2 = st.columns(2)
        with c1:
            section("\u26A0\uFE0F High Relegation Risk")
            st.dataframe(df[df["Tier"]=="TOP"].nlargest(25,"Relegation Risk")[["Player ID","Name","Primary Sport","Age","Overall Rating","Relegation Risk","Performance Trend","Attendance %"]], use_container_width=True)
        with c2:
            section("\U0001F31F Strong Promotion Candidates")
            st.dataframe(df[df["Tier"]=="PIPELINE"].nlargest(25,"Promotion Chance")[["Player ID","Name","Primary Sport","Age","Overall Rating","Promotion Chance","Performance Trend","Total Medals"]], use_container_width=True)
        section("Tier Distribution by Sport")
        ts = df.groupby(["Primary Sport","Tier"]).size().reset_index(name="Count")
        fig = px.bar(ts, x="Primary Sport", y="Count", color="Tier", barmode="group", color_discrete_map={"TOP": GREEN, "PIPELINE": GOLD}, text="Count")
        fig.update_layout(xaxis_tickangle=-45, **PL); st.plotly_chart(fig, use_container_width=True)
    with t2:
        section("What-If Simulation")
        c1, c2 = st.columns(2)
        with c1: top_thresh = st.slider("Top Tier Min Rating (relegation)", 55, 95, 72)
        with c2: pipe_thresh = st.slider("Pipeline Promotion Threshold", 55, 90, 68)
        rel = df[(df["Tier"]=="TOP") & (df["Overall Rating"]<top_thresh)]
        prom = df[(df["Tier"]=="PIPELINE") & (df["Overall Rating"]>=pipe_thresh)]
        kpi_row([(str(len(rel)), "Relegated", f"From Top 400", "down"), (str(len(prom)), "Promoted", f"From Pipeline", "up"), (f"{len(prom)-len(rel):+d}", "Net Movement", "", "up" if len(prom)>=len(rel) else "down")])
        if len(rel)>0:
            section(f"{len(rel)} At Relegation Risk")
            st.dataframe(rel[["Player ID","Name","Primary Sport","District","Overall Rating","Performance Trend"]].sort_values("Overall Rating"), use_container_width=True)
        if len(prom)>0:
            section(f"{len(prom)} Ready for Promotion")
            st.dataframe(prom[["Player ID","Name","Primary Sport","District","Overall Rating","Performance Trend"]].sort_values("Overall Rating", ascending=False), use_container_width=True)
    with t3:
        section("Rating Distribution - Tier Overlap")
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df[df["Tier"]=="TOP"]["Overall Rating"], name="Top Tier", marker_color=GREEN, opacity=0.7, nbinsx=25))
        fig.add_trace(go.Histogram(x=df[df["Tier"]=="PIPELINE"]["Overall Rating"], name="Pipeline", marker_color=GOLD, opacity=0.7, nbinsx=25))
        fig.update_layout(barmode="overlay", title="Rating Overlap", **PL); st.plotly_chart(fig, use_container_width=True)
        ol = len(df[(df["Tier"]=="PIPELINE") & (df["Overall Rating"]>=df[df["Tier"]=="TOP"]["Overall Rating"].min())])
        st.info(f"**{ol}** pipeline athletes within top tier range.")
        section("Stipend Analysis")
        sd = df[df["Tier"]=="TOP"]["Stipend (BDT)"].value_counts().reset_index()
        sd.columns = ["Stipend (BDT)","Count"]
        fig = px.pie(sd, values="Count", names="Stipend (BDT)", title="Stipend Distribution", color_discrete_sequence=[GREEN,"#198754","#0D6EFD","#6F42C1"], hole=0.35)
        fig.update_traces(textinfo="label+value+percent"); fig.update_layout(**PL); st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"**Total Monthly Budget: \u09F3 {df[df['Tier']=='TOP']['Stipend (BDT)'].sum():,.0f}**")

# ============ DISTRICT ANALYTICS ============
elif page == "\U0001F5FA  District Analytics":
    header("District Analytics", "Performance breakdown by administrative districts")
    sel = st.selectbox("District", ["\U0001F30D All Districts"] + district_list)
    if sel == "\U0001F30D All Districts":
        st.dataframe(district_summary.sort_values("Avg_Rating", ascending=False), use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(district_summary.sort_values("Avg_Rating", ascending=False), x="District", y="Avg_Rating", color="Avg_Rating", color_continuous_scale="RdYlGn", range_color=[55,80], title="Performance Rankings", text="Avg_Rating")
            fig.update_layout(xaxis_tickangle=-45, **PL); st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.scatter(district_summary, x="Top_Tier", y="Avg_Rating", size="Total_Athletes", hover_name="District", text="District", title="Top Tier vs Rating", color="Total_Medals", color_continuous_scale="YlOrRd", size_max=30)
            fig.update_traces(textposition="top center", textfont_size=9); fig.update_layout(**PL); st.plotly_chart(fig, use_container_width=True)
        fig = px.bar(district_summary, x="District", y=["Male","Female"], barmode="group", title="Gender by District", color_discrete_map={"Male": GREEN, "Female": RED})
        fig.update_layout(xaxis_tickangle=-45, **PL); st.plotly_chart(fig, use_container_width=True)
        fig = px.bar(district_summary.sort_values("Total_Stipend", ascending=False), x="District", y="Total_Stipend", title="Stipend by District", color="Total_Stipend", color_continuous_scale="Greens", text="Total_Stipend")
        fig.update_layout(xaxis_tickangle=-45, **PL); fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside"); st.plotly_chart(fig, use_container_width=True)
    else:
        dd = df[df["District"]==sel]
        section(f"{sel} Overview")
        kpi_row([(str(len(dd)), "Athletes", "", "up"), (f"{dd['Overall Rating'].mean():.1f}", "Avg Rating", "", "up"), (str((dd["Tier"]=="TOP").sum()), "Top Tier", "", "up"), (str(dd["Total Medals"].sum()), "Medals", "", "up"), (f"\u09F3{dd['Stipend (BDT)'].sum():,.0f}", "Stipend", "", "up")])
        c1, c2 = st.columns(2)
        with c1:
            sd = dd["Primary Sport"].value_counts()
            fig = px.pie(values=sd.values, names=sd.index, title=f"Sports - {sel}", hole=0.35)
            fig.update_traces(textinfo="label+value+percent"); st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.box(dd, x="Primary Sport", y="Overall Rating", title=f"Rating by Sport - {sel}")
            fig.update_layout(**PL); st.plotly_chart(fig, use_container_width=True)
        section(f"Athletes from {sel}")
        st.dataframe(dd[["Player ID","Name","Gender","Age","Primary Sport","Tier","Overall Rating","Total Medals","Stipend (BDT)","Status"]].sort_values("Overall Rating", ascending=False), use_container_width=True)

# ============ SPORT ANALYTICS ============
elif page == "\U0001F3C6  Sport Analytics":
    header("Sport Analytics", "Deep dive into each of the 10 Notun Kuri sports")
    sel = st.selectbox("Sport", sport_list)
    sd = df[df["Primary Sport"]==sel]
    rc = f"Rating - {sel}"
    kpi_row([(str(len(sd)), "Athletes", "", "up"), (f"{sd[rc].mean():.1f}", "Avg Rating", "", "up"), (f"{sd[rc].max():.1f}", "Top Rating", "", "up"), (str(sd["Total Medals"].sum()), "Medals", f"{sd['Gold Medals'].sum()} gold", "up"), (f"{sd['Training Hours/Week'].mean():.1f}", "Avg Training", "", "up"), (f"{sd['Attendance %'].mean():.1f}%", "Avg Attendance", "", "up")])
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(sd, x=rc, nbins=25, title=f"Rating - {sel}", color="Tier", color_discrete_map={"TOP": GREEN, "PIPELINE": GOLD}, opacity=0.75)
        fig.update_layout(**PL); st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.box(sd, x="Gender", y=rc, color="Gender", title=f"Gender - {sel}", color_discrete_map={"Male": GREEN, "Female": RED})
        fig.update_layout(**PL); st.plotly_chart(fig, use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(sd, x="Training Hours/Week", y=rc, color="Tier", size="Tournaments Played", opacity=0.7, title=f"Training vs Rating - {sel}", color_discrete_map={"TOP": GREEN, "PIPELINE": GOLD}, size_max=20)
        fig.update_layout(**PL); st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.scatter(sd, x="Age", y=rc, color="Gender", size="Total Medals", opacity=0.7, title=f"Age vs Rating - {sel}", color_discrete_map={"Male": GREEN, "Female": RED}, size_max=20)
        fig.update_layout(**PL); st.plotly_chart(fig, use_container_width=True)
    fig = px.scatter(sd, x="Performance Trend", y=rc, color="Tier", size="Attendance %", hover_name="Name", title=f"Trend vs Rating - {sel}", color_discrete_map={"TOP": GREEN, "PIPELINE": GOLD}, size_max=15)
    fig.update_layout(**PL); st.plotly_chart(fig, use_container_width=True)
    section(f"Top 15 in {sel}")
    st.dataframe(sd.nlargest(15, rc)[["Player ID","Name","Gender","Age","District","Tier",rc,"Total Medals","Performance Trend","Training Hours/Week","Coach Remarks"]], use_container_width=True)

# ============ MINISTRY REPORTS ============
elif page == "\U0001F4CB  Ministry Reports":
    header("Official Ministry Reports", "Executive summaries for the Ministry of Sports & Youth Affairs", ["Confidential", "Government of Bangladesh"])
    t1, t2, t3 = st.tabs(["\U0001F4CC Executive Summary", "\U0001F3C6 Sport Report", "\U0001F4E5 Export"])
    with t1:
        st.markdown(f"""<div class="report-header"><h2>\U0001F1E7\U0001F1E9 Executive Summary</h2><p>Notun Kuri National Talent Stipend Program \u2022 Ministry of Sports & Youth Affairs \u2022 Government of Bangladesh</p></div>""", unsafe_allow_html=True)
        top_df = df[df["Tier"]=="TOP"]; pipe_df = df[df["Tier"]=="PIPELINE"]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"### Program Statistics\n| Metric | Value |\n|--------|-------|\n| Total Athletes | **{len(df)}** |\n| Top Tier (Stipend) | **{len(top_df)}** |\n| Pipeline Tier | **{len(pipe_df)}** |\n| Male | **{(df['Gender']=='Male').sum()}** ({(df['Gender']=='Male').mean()*100:.1f}%) |\n| Female | **{(df['Gender']=='Female').sum()}** ({(df['Gender']=='Female').mean()*100:.1f}%) |\n| Age Range | **{df['Age'].min()}-{df['Age'].max()}** years |\n| Avg Age | **{df['Age'].mean():.1f}** years |\n| Districts | **{df['District'].nunique()}** |\n| Sports | **{len(sport_list)}** |")
        with c2:
            st.markdown(f"### Performance Metrics\n| Metric | Value |\n|--------|-------|\n| Avg Rating | **{df['Overall Rating'].mean():.1f}** |\n| Avg Training | **{df['Training Hours/Week'].mean():.1f}** hrs/wk |\n| Avg Attendance | **{df['Attendance %'].mean():.1f}%** |\n| Gold Medals | **{df['Gold Medals'].sum()}** |\n| Silver Medals | **{df['Silver Medals'].sum()}** |\n| Bronze Medals | **{df['Bronze Medals'].sum()}** |\n| Active | **{(df['Status']=='Active').sum()}** |\n| Recovering | **{(df['Status']=='Recovering').sum()}** |\n| Monthly Budget | **\u09F3 {top_df['Stipend (BDT)'].sum():,.0f}** |")
        st.divider()
        fig = make_subplots(rows=1, cols=3, subplot_titles=["Tier Split", "Sports", "Gender"], specs=[[{"type":"pie"},{"type":"pie"},{"type":"pie"}]])
        fig.add_trace(go.Pie(labels=["Top","Pipeline"], values=[len(top_df),len(pipe_df)], marker_colors=[GREEN,GOLD]), row=1, col=1)
        sc = df["Primary Sport"].value_counts()
        fig.add_trace(go.Pie(labels=sc.index, values=sc.values), row=1, col=2)
        gc = df["Gender"].value_counts()
        fig.add_trace(go.Pie(labels=gc.index, values=gc.values, marker_colors=[GREEN,RED]), row=1, col=3)
        fig.update_layout(height=400, showlegend=True); st.plotly_chart(fig, use_container_width=True)
    with t2:
        section("Sport-Wise Report")
        st.dataframe(sport_summary, use_container_width=True)
        for sp in sport_list:
            sdf = df[df["Primary Sport"]==sp]; rc = f"Rating - {sp}"
            with st.expander(f"**{sp}** \u2014 {len(sdf)} athletes | Avg: {sdf[rc].mean():.1f}"):
                kpi_row([(str(len(sdf)), "Athletes", "", "up"), (f"{sdf[rc].mean():.1f}", "Avg Rating", "", "up"), (str((sdf["Tier"]=="TOP").sum()), "Top Tier", "", "up"), (str(sdf["Total Medals"].sum()), "Medals", "", "up")])
                st.dataframe(sdf.nlargest(3, rc)[["Player ID","Name","Gender","Age",rc,"Tier"]], use_container_width=True, hide_index=True)
    with t3:
        section("Export Data")
        c1, c2, c3 = st.columns(3)
        with c1: st.download_button("Full Dataset", df.to_csv(index=False), "notun_kuri_full.csv", "text/csv", use_container_width=True)
        with c2: st.download_button("Top 400", df[df["Tier"]=="TOP"].to_csv(index=False), "top400.csv", "text/csv", use_container_width=True)
        with c3: st.download_button("Pipeline 400", df[df["Tier"]=="PIPELINE"].to_csv(index=False), "pipeline400.csv", "text/csv", use_container_width=True)
        st.divider()
        st.dataframe(district_summary, use_container_width=True)
        st.download_button("District Summary", district_summary.to_csv(index=False), "district_summary.csv", "text/csv")

# ============ FOOTER ============
st.divider()
st.markdown("""<div style="text-align:center; color:#6C757D; padding:1rem;">
    <p style="margin:0;">\U0001F1E7\U0001F1E9 <strong>Notun Kuri - National Talent Stipend Program</strong></p>
    <p style="margin:0;">Ministry of Sports & Youth Affairs | Government of Bangladesh</p>
    <p style="margin:0; font-size:0.75rem;">Confidential - For Official Use Only | Dashboard v2.0</p>
</div>""", unsafe_allow_html=True)
