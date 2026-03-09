"""
EVERA B2B Client Pipeline Dashboard
TREV Brand Teardown Project — v1.4
Junior Research Assistant Output | All data from uploaded B2B_CLIENT_LIST_.xlsx
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EVERA | B2B Pipeline Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0D0F14;
    color: #E8EAF0;
}

.main { background-color: #0D0F14; }

h1, h2, h3 { font-family: 'Syne', sans-serif; }

.metric-card {
    background: linear-gradient(135deg, #1A1D26 0%, #141720 100%);
    border: 1px solid #2A2E3D;
    border-left: 4px solid #00D4AA;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.metric-card h2 {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #00D4AA;
    margin: 0;
}
.metric-card p {
    color: #8B90A0;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 4px 0 0 0;
}

.win-card {
    border-left-color: #4ADE80;
}
.win-card h2 { color: #4ADE80; }

.pipeline-card {
    border-left-color: #FACC15;
}
.pipeline-card h2 { color: #FACC15; }

.p1-card {
    border-left-color: #818CF8;
}
.p1-card h2 { color: #818CF8; }

.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #E8EAF0;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 32px 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #2A2E3D;
}

.stDataFrame { border-radius: 10px; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0F1119;
    border-right: 1px solid #1E2130;
}

.stage-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ─── DATA LOADING ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    # P0 Clients (columns A–J)
    p0_cols = {
        'S.No': 0, 'Opportunity': 1, 'Priority': 2, 'Use case': 3,
        'Outreach': 4, 'Stage': 5, 'Industry': 6,
        'Monthly Revenue (INR)': 7, 'Cars Required': 8, 'Timeline': 9
    }
    # P1 / Pipeline Clients (columns K–S, i.e. 10–18)
    p1_cols = {
        'S.No': 10, 'Opportunity': 11, 'Priority': 12, 'Use case': 13,
        'Outreach': 14, 'Stage': 15,
        'Monthly Revenue (INR)': 16, 'Cars Required': 17, 'Timeline': 18
    }

    raw = pd.read_excel(file, header=0, sheet_name="Sheet1")

    def extract_segment(df, col_map, default_priority=None):
        subset = df.iloc[:, list(col_map.values())].copy()
        subset.columns = list(col_map.keys())
        subset = subset[subset['Opportunity'].notna()].copy()
        # Exclude totals rows (numeric S.No only)
        subset = subset[subset['Opportunity'].astype(str).str.strip() != '']
        subset = subset[~subset['Opportunity'].astype(str).str.lower().str.contains('partner|total', na=False)]
        if default_priority:
            subset['Priority'] = subset['Priority'].fillna(default_priority)
        subset['Monthly Revenue (INR)'] = pd.to_numeric(subset['Monthly Revenue (INR)'], errors='coerce').fillna(0)
        subset['Cars Required'] = pd.to_numeric(subset['Cars Required'], errors='coerce').fillna(0)
        return subset

    df_p0 = extract_segment(raw, p0_cols)
    df_p0['Segment'] = 'Current Pipeline (P0)'

    df_p1 = extract_segment(raw, p1_cols)
    df_p1['Segment'] = 'Future Pipeline (P1)'
    # Add Industry for P1 (not in original — mark as Unknown)
    if 'Industry' not in df_p1.columns:
        df_p1['Industry'] = 'N/A'

    df = pd.concat([df_p0, df_p1], ignore_index=True)
    df['Opportunity'] = df['Opportunity'].astype(str).str.strip()
    df['Stage'] = df['Stage'].astype(str).str.strip()
    df['Priority'] = df['Priority'].astype(str).str.strip()
    df['Industry'] = df['Industry'].astype(str).str.strip() if 'Industry' in df.columns else 'N/A'
    df['Use case'] = df['Use case'].fillna('N/A')
    df['Timeline'] = df['Timeline'].fillna('TBD')
    return df

# ─── SIDEBAR (uploader first, filters after data loads) ──────────────────────
with st.sidebar:
    st.markdown("### ⚡ EVERA B2B Pipeline")
    st.markdown("*TREV Brand Teardown — v1.4*")
    st.divider()
    uploaded_file = st.file_uploader("📂 Upload B2B_CLIENT_LIST_.xlsx", type=["xlsx"])
    st.divider()
    view = st.radio("View", ["Dashboard", "Client Table", "Pipeline Details"])

if uploaded_file is None:
    st.info("👈 Upload **B2B_CLIENT_LIST_.xlsx** in the sidebar to load the dashboard.")
    st.stop()

df = load_data(uploaded_file)

# ─── DERIVED FIELDS ──────────────────────────────────────────────────────────
STAGE_ORDER = ['Evera Wins', 'Contract Signing', 'Verbal Ok | Negotiation',
               'Proposal', 'Need Assessment', 'Discovery', 'Cross-sell/Upsell Existing']

STAGE_COLORS = {
    'Evera Wins': '#4ADE80',
    'Contract Signing': '#34D399',
    'Verbal Ok | Negotiation': '#60A5FA',
    'Proposal': '#FACC15',
    'Need Assessment': '#FB923C',
    'Discovery': '#C084FC',
    'Cross-sell/Upsell Existing': '#38BDF8',
}

df['Stage_Clean'] = df['Stage'].str.strip().str.replace('\xa0', '', regex=False)

p0 = df[df['Segment'] == 'Current Pipeline (P0)']
p1 = df[df['Segment'] == 'Future Pipeline (P1)']

with st.sidebar:
    st.divider()
    st.markdown("**Filter by Stage**")
    stages = sorted(df['Stage_Clean'].unique().tolist())
    selected_stages = st.multiselect("Stage", stages, default=stages)
    st.markdown("**Filter by Priority**")
    priorities = sorted(df['Priority'].unique().tolist())
    selected_priorities = st.multiselect("Priority", priorities, default=priorities)
    st.divider()
    st.caption("Source: B2B_CLIENT_LIST_.xlsx\nData verified from uploaded file only.\nNo fabricated data.")

filtered = df[
    df['Stage_Clean'].isin(selected_stages) &
    df['Priority'].isin(selected_priorities)
]

# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────
st.markdown("# ⚡ EVERA B2B Client Pipeline")
st.markdown("*Competitive proxy data for TREV Brand Teardown — TREV Project v1.4*")

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
total_rev = df['Monthly Revenue (INR)'].sum()
total_cars = int(df['Cars Required'].sum())
wins = df[df['Stage_Clean'] == 'Evera Wins']
wins_rev = wins['Monthly Revenue (INR)'].sum()
pipeline_p0_rev = p0['Monthly Revenue (INR)'].sum()
p1_rev = p1['Monthly Revenue (INR)'].sum()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <h2>₹{total_rev/1e6:.1f}M</h2>
        <p>Total Monthly Revenue Potential</p>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card win-card">
        <h2>₹{wins_rev/1e6:.1f}M</h2>
        <p>Won — Live Revenue ({len(wins)} clients)</p>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card pipeline-card">
        <h2>{total_cars}</h2>
        <p>Total EV Cars Required</p>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card p1-card">
        <h2>₹{p1_rev/1e6:.1f}M</h2>
        <p>Future Pipeline Potential (P1)</p>
    </div>""", unsafe_allow_html=True)

st.divider()

# ── DASHBOARD VIEW ────────────────────────────────────────────────────────────
if view == "Dashboard":

    col_a, col_b = st.columns([1.2, 1])

    with col_a:
        st.markdown('<div class="section-header">Revenue by Stage</div>', unsafe_allow_html=True)
        stage_rev = (
            filtered.groupby('Stage_Clean')['Monthly Revenue (INR)']
            .sum()
            .reset_index()
            .sort_values('Monthly Revenue (INR)', ascending=True)
        )
        colors = [STAGE_COLORS.get(s, '#8B90A0') for s in stage_rev['Stage_Clean']]
        fig_bar = go.Figure(go.Bar(
            x=stage_rev['Monthly Revenue (INR)'],
            y=stage_rev['Stage_Clean'],
            orientation='h',
            marker_color=colors,
            text=[f"₹{v/1e5:.1f}L" for v in stage_rev['Monthly Revenue (INR)']],
            textposition='outside',
        ))
        fig_bar.update_layout(
            plot_bgcolor='#1A1D26', paper_bgcolor='#1A1D26',
            font_color='#E8EAF0', font_family='DM Sans',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False),
            margin=dict(l=0, r=60, t=10, b=10),
            height=340,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Industry Mix (P0)</div>', unsafe_allow_html=True)
        ind_rev = (
            p0[p0['Industry'].notna() & (p0['Industry'] != 'nan')]
            .groupby('Industry')['Monthly Revenue (INR)']
            .sum()
            .reset_index()
            .sort_values('Monthly Revenue (INR)', ascending=False)
        )
        fig_pie = px.pie(
            ind_rev, values='Monthly Revenue (INR)', names='Industry',
            hole=0.55,
            color_discrete_sequence=['#00D4AA','#4ADE80','#60A5FA','#FACC15',
                                      '#FB923C','#C084FC','#38BDF8','#F87171']
        )
        fig_pie.update_traces(textinfo='label+percent', textfont_size=11)
        fig_pie.update_layout(
            plot_bgcolor='#1A1D26', paper_bgcolor='#1A1D26',
            font_color='#E8EAF0', font_family='DM Sans',
            showlegend=False,
            margin=dict(l=0, r=0, t=10, b=10),
            height=340,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Stage funnel
    st.markdown('<div class="section-header">Pipeline Funnel — P0 Current Clients</div>', unsafe_allow_html=True)
    funnel_order = ['Discovery', 'Need Assessment', 'Proposal',
                    'Verbal Ok | Negotiation', 'Contract Signing', 'Evera Wins']
    funnel_data = (
        p0.groupby('Stage_Clean').agg(
            Count=('Opportunity', 'count'),
            Revenue=('Monthly Revenue (INR)', 'sum')
        ).reindex([s for s in funnel_order if s in p0['Stage_Clean'].unique()])
        .reset_index()
        .dropna()
    )
    fig_funnel = go.Figure(go.Funnel(
        y=funnel_data['Stage_Clean'],
        x=funnel_data['Count'],
        textinfo='value+percent initial',
        marker_color=[STAGE_COLORS.get(s, '#8B90A0') for s in funnel_data['Stage_Clean']],
        connector={'line': {'color': '#2A2E3D', 'width': 2}},
    ))
    fig_funnel.update_layout(
        plot_bgcolor='#1A1D26', paper_bgcolor='#1A1D26',
        font_color='#E8EAF0', font_family='DM Sans',
        margin=dict(l=0, r=0, t=10, b=10),
        height=320,
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

    # Use case breakdown
    st.markdown('<div class="section-header">Use Case Frequency</div>', unsafe_allow_html=True)
    use_cases = []
    for _, row in filtered.iterrows():
        for uc in str(row['Use case']).split(','):
            uc = uc.strip()
            if uc and uc != 'nan':
                use_cases.append({'Use Case': uc, 'Revenue': row['Monthly Revenue (INR)']})
    uc_df = pd.DataFrame(use_cases)
    if not uc_df.empty:
        uc_agg = uc_df.groupby('Use Case').agg(Count=('Use Case', 'count'), Revenue=('Revenue', 'sum')).reset_index().sort_values('Revenue', ascending=False)
        fig_uc = px.bar(uc_agg, x='Use Case', y='Revenue',
                        text=uc_agg['Revenue'].apply(lambda v: f"₹{v/1e5:.0f}L"),
                        color='Count',
                        color_continuous_scale=['#1A1D26', '#00D4AA'])
        fig_uc.update_layout(
            plot_bgcolor='#1A1D26', paper_bgcolor='#1A1D26',
            font_color='#E8EAF0', font_family='DM Sans',
            xaxis_title='', yaxis_title='Monthly Revenue (INR)',
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=10),
            height=300,
        )
        fig_uc.update_traces(textposition='outside')
        st.plotly_chart(fig_uc, use_container_width=True)


# ── CLIENT TABLE VIEW ─────────────────────────────────────────────────────────
elif view == "Client Table":
    st.markdown('<div class="section-header">All B2B Clients</div>', unsafe_allow_html=True)

    show_df = filtered[[
        'Opportunity', 'Priority', 'Segment', 'Stage_Clean', 'Industry',
        'Use case', 'Monthly Revenue (INR)', 'Cars Required', 'Timeline'
    ]].copy()
    show_df.columns = [
        'Client', 'Priority', 'Segment', 'Stage', 'Industry',
        'Use Case', 'Monthly Rev (INR)', 'Cars', 'Timeline'
    ]
    show_df['Monthly Rev (INR)'] = show_df['Monthly Rev (INR)'].apply(lambda x: f"₹{int(x):,}")
    show_df['Cars'] = show_df['Cars'].astype(int)
    show_df = show_df.sort_values(['Priority', 'Stage'])

    st.dataframe(show_df, use_container_width=True, height=540)

    st.download_button(
        label="⬇ Download Filtered CSV",
        data=show_df.to_csv(index=False).encode(),
        file_name="evera_b2b_clients_filtered.csv",
        mime="text/csv"
    )


# ── PIPELINE DETAILS VIEW ─────────────────────────────────────────────────────
elif view == "Pipeline Details":
    st.markdown('<div class="section-header">P0 — Current Priority Pipeline</div>', unsafe_allow_html=True)

    for stage in ['Evera Wins', 'Contract Signing', 'Verbal Ok | Negotiation',
                  'Proposal', 'Need Assessment', 'Discovery']:
        group = p0[p0['Stage_Clean'].str.contains(stage.split('|')[0].strip(), na=False)]
        if group.empty:
            continue
        color = STAGE_COLORS.get(stage, '#8B90A0')
        with st.expander(f"🔹 {stage}  ({len(group)} clients | ₹{group['Monthly Revenue (INR)'].sum()/1e5:.1f}L/mo)"):
            for _, row in group.iterrows():
                st.markdown(f"""
                **{row['Opportunity']}** &nbsp;|&nbsp; {row['Industry']} &nbsp;|&nbsp;
                _{row['Use case']}_ &nbsp;|&nbsp;
                🚗 {int(row['Cars Required'])} cars &nbsp;|&nbsp;
                💰 ₹{int(row['Monthly Revenue (INR)']):,}/mo &nbsp;|&nbsp;
                📅 {row['Timeline']}
                """)

    st.markdown('<div class="section-header">P1 — Future Pipeline (Q2–Q3 Target)</div>', unsafe_allow_html=True)

    p1_display = p1[['Opportunity', 'Priority', 'Stage_Clean', 'Use case',
                       'Monthly Revenue (INR)', 'Cars Required', 'Timeline']].copy()
    p1_display.columns = ['Client', 'Priority', 'Stage', 'Use Case', 'Monthly Rev (INR)', 'Cars', 'Timeline']
    p1_display['Monthly Rev (INR)'] = p1_display['Monthly Rev (INR)'].apply(lambda x: f"₹{int(x):,}")
    p1_display['Cars'] = p1_display['Cars'].astype(int)
    st.dataframe(p1_display, use_container_width=True, height=400)

    st.info(f"**P1 Total Potential:** ₹{p1_rev/1e5:.1f}L/mo across {int(p1['Cars Required'].sum())} cars — targeted for Q2–Q3 launch.")
