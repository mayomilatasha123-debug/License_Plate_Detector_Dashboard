import streamlit as st
import sqlite3
import pandas as pd
import os
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="LPD | License Plate Detector",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)
st_autorefresh(interval=5000, key="datarefresh")

# ============================================================
# THEME — single navy accent, dark background, minimal chrome
# ============================================================
st.markdown("""
<style>
    :root {
        --navy-bg: #0b1220;
        --navy-panel: #121a2c;
        --navy-panel-2: #17213a;
        --navy-border: #223252;
        --accent: #3b82f6;
        --accent-light: #60a5fa;
        --text-primary: #e6ecf5;
        --text-secondary: #8ea0bd;
    }

    .stApp { background-color: var(--navy-bg); }

    div[data-testid="stAppViewContainer"] .block-container {
        padding-top: 1.2rem;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] { background: transparent; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--navy-panel);
        border-right: 1px solid var(--navy-border);
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: var(--text-primary) !important;
    }

    /* Custom header bar */
    .po-header {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 0 0 14px 0;
        border-bottom: 1px solid var(--navy-border);
        margin-bottom: 24px;
    }
    .po-logo {
        width: 50px;
        height: 50px;
        border-radius: 14px;
        background: linear-gradient(150deg, #1b2b52, #0b1220);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        position: relative;
        box-shadow: 0 0 0 1px var(--navy-border), 0 0 18px rgba(59,130,246,0.35);
        overflow: hidden;
    }
    .po-logo svg { position: relative; z-index: 2; }
    .po-logo::after {
        content: "";
        position: absolute;
        top: -30%; left: -30%;
        width: 160%; height: 160%;
        background: conic-gradient(from 0deg, transparent, var(--accent), transparent 35%);
        animation: po-spin 3.5s linear infinite;
        opacity: 0.55;
    }
    @keyframes po-spin { to { transform: rotate(360deg); } }
    .po-title h1 {
        font-size: 27px;
        font-weight: 800;
        color: var(--text-primary);
        margin: 0;
        letter-spacing: 1.5px;
        line-height: 1.15;
    }
    .po-title p {
        font-size: 13px;
        color: var(--text-secondary);
        margin: 0;
    }
    .po-status {
        margin-left: auto;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        color: var(--text-secondary);
    }
    .po-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--accent-light);
        box-shadow: 0 0 8px var(--accent-light);
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: var(--navy-panel);
        border: 1px solid var(--navy-border);
        border-radius: 10px;
        padding: 18px 20px;
    }
    div[data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricValue"] {
        color: var(--accent-light) !important;
        font-size: 38px !important;
        font-weight: 800 !important;
    }

    /* Bordered containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--navy-panel);
        border: 1px solid var(--navy-border) !important;
        border-radius: 10px;
    }

    h1, h2, h3 { color: var(--text-primary) !important; }
    p, span, label { color: var(--text-secondary); }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--navy-border);
        border-radius: 10px;
        overflow: hidden;
    }

    .stButton > button {
        background-color: var(--accent);
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
    }
    .stButton > button:hover { background-color: var(--accent-light); }

    hr { border-color: var(--navy-border) !important; }

    .stSlider > div > div > div > div { background-color: var(--accent) !important; }

    div[data-baseweb="select"] > div {
        background-color: var(--navy-panel-2);
        border-color: var(--navy-border);
    }

    .po-caption {
        color: var(--text-secondary);
        font-size: 12.5px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'detections.db')

@st.cache_data(ttl=5)
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM detections ORDER BY timestamp DESC", conn)
    conn.close()
    return df

df = load_data()

if 'id' not in df.columns:
    df = df.reset_index().rename(columns={'index': 'id'})

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="po-header">
    <div class="po-logo">
        <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="2" y="9" width="24" height="10" rx="3" stroke="#60a5fa" stroke-width="2"/>
            <circle cx="8.5" cy="14" r="2.1" fill="#60a5fa"/>
            <line x1="13" y1="14" x2="23" y2="14" stroke="#3b82f6" stroke-width="1.6" stroke-dasharray="1.5 2.2"/>
            <path d="M4 5 L9 5 M19 5 L24 5 M4 23 L9 23 M19 23 L24 23"
                  stroke="#60a5fa" stroke-width="1.6" stroke-linecap="round"/>
        </svg>
    </div>
    <div class="po-title">
        <h1>LPD</h1>
        <p>License Plate Detector</p>
    </div>
    <div class="po-status"><span class="po-dot"></span>Live · auto-refreshing</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR — filters
# ============================================================
st.sidebar.markdown("### Filters")
st.sidebar.markdown("---")

vehicle_conf_min = st.sidebar.slider("Vehicle Confidence", 0.0, 1.0, 0.0)
plate_conf_min = st.sidebar.slider("Plate Confidence", 0.0, 1.0, 0.0)
ocr_conf_min = st.sidebar.slider("OCR Confidence", 0.0, 1.0, 0.0)
search_plate = st.sidebar.text_input("Search Plate Number")

filtered_df = df[
    (df['vehicle_confidence'] >= vehicle_conf_min) &
    (df['plate_confidence'] >= plate_conf_min) &
    (df['ocr_confidence'] >= ocr_conf_min)
]
if search_plate:
    filtered_df = filtered_df[filtered_df['plate_number'].str.contains(search_plate, case=False, na=False)]

# ============================================================
# METRICS
# ============================================================
col1, col2, col3, col4 = st.columns(4)
total_count = len(df)
today_count = len(df[pd.to_datetime(df['timestamp']).dt.date == pd.Timestamp.now().date()])
avg_conf = round(df['ocr_confidence'].mean() * 100, 1) if not df.empty else 0
unreadable_count = len(df[df['plate_number'] == 'unreadable'])

col1.metric("Total Detections", total_count)
col2.metric("Today", today_count)
col3.metric("Avg OCR Confidence", f"{avg_conf}%")
col4.metric("Unreadable Plates", unreadable_count)

st.markdown("---")

# ============================================================
# RECORD SELECTOR + DETAIL VIEW
# ============================================================
st.markdown("### Detection Viewer")

if not filtered_df.empty:
    def label_for(row):
        return f"#{row['id']}  ·  {row['plate_number']}  ·  {row['timestamp']}"

    options = filtered_df.apply(label_for, axis=1).tolist()
    selected_label = st.selectbox("Select a detection to view", options, index=0)
    selected_row = filtered_df.iloc[options.index(selected_label)]
else:
    selected_row = None
    st.info("No detections match the current filters")

with st.container(border=True):
    img_col, info_col = st.columns([1, 1.6])

    with img_col:
        st.markdown("**Preview**")
        if selected_row is not None:
            st.image(selected_row['image_path'], use_container_width=True)
        else:
            st.markdown('<p class="po-caption">Nothing to display</p>', unsafe_allow_html=True)

    with info_col:
        st.markdown("**Detection Details**")
        if selected_row is not None:
            st.markdown(f"**Plate Number:** {selected_row['plate_number']}")
            st.progress(selected_row['vehicle_confidence'], text=f"Vehicle Confidence: {selected_row['vehicle_confidence']*100:.0f}%")
            st.progress(selected_row['plate_confidence'], text=f"Plate Confidence: {selected_row['plate_confidence']*100:.0f}%")
            st.progress(selected_row['ocr_confidence'], text=f"OCR Confidence: {selected_row['ocr_confidence']*100:.0f}%")
            st.markdown(f'<p class="po-caption">Detected: {selected_row["timestamp"]}</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="po-caption">—</p>', unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# CHARTS
# ============================================================
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("### Detections Over Time")
    time_df = df.copy()
    time_df['date'] = pd.to_datetime(time_df['timestamp']).dt.date
    daily_counts = time_df.groupby('date').size()
    st.line_chart(daily_counts, color="#3b82f6")

with chart_col2:
    st.markdown("### Confidence Distribution")
    st.bar_chart(df[['vehicle_confidence', 'plate_confidence', 'ocr_confidence']], color=["#3b82f6", "#60a5fa", "#16244a"])

st.markdown("---")

# ============================================================
# TABLE
# ============================================================
st.markdown("### Recent Detections")

st.dataframe(
    filtered_df,
    column_config={
        "plate_confidence": st.column_config.ProgressColumn("Plate Confidence", min_value=0, max_value=1),
        "ocr_confidence": st.column_config.ProgressColumn("OCR Confidence", min_value=0, max_value=1),
        "vehicle_confidence": st.column_config.ProgressColumn("Vehicle Confidence", min_value=0, max_value=1),
        "image_path": st.column_config.ImageColumn("Preview"),
    },
    use_container_width=True,
    hide_index=True
)
