import streamlit as st

THEMES = {
    "Neon Cyberpunk": {
        "bg": "#09090b", "card_bg": "#18181b", "sidebar_bg": "#09090b", "border": "#27272a",
        "primary": "#f472b6", "secondary": "#22d3ee", "text_primary": "#f8fafc", "text_secondary": "#a1a1aa",
        "chart_colors": ['#f472b6', '#22d3ee', '#a855f7', '#fb923c', '#4ade80'],
        "plotly_template": "plotly_dark"
    },
    "Matcha Cloud": {
        "bg": "#fafaf9", "card_bg": "#ffffff", "sidebar_bg": "#f5f5f4", "border": "#e7e5e4",
        "primary": "#a3e635", "secondary": "#fbcfe8", "text_primary": "#1c1917", "text_secondary": "#78716c",
        "chart_colors": ['#a3e635', '#fbcfe8', '#bfdbfe', '#fde047', '#c4b5fd'],
        "plotly_template": "plotly_white"
    },
    "Y2K Vaporwave": {
        "bg": "#1e1b4b", "card_bg": "#312e81", "sidebar_bg": "#2e1065", "border": "#4c1d95",
        "primary": "#ff00ff", "secondary": "#00ffff", "text_primary": "#ffffff", "text_secondary": "#c7d2fe",
        "chart_colors": ['#ff00ff', '#00ffff', '#fbbf24', '#f43f5e', '#8b5cf6'],
        "plotly_template": "plotly_dark"
    },
    "Dark Espresso": {
        "bg": "#1c1917", "card_bg": "#292524", "sidebar_bg": "#1c1917", "border": "#44403c",
        "primary": "#d97706", "secondary": "#fcd34d", "text_primary": "#fafaf9", "text_secondary": "#a8a29e",
        "chart_colors": ['#d97706', '#fcd34d', '#78350f', '#fb923c', '#b45309'],
        "plotly_template": "plotly_dark"
    },
    "Enterprise Light": {
        "bg": "#F8FAFC", "card_bg": "#FFFFFF", "sidebar_bg": "#F1F5F9", "border": "#E2E8F0",
        "primary": "#2563EB", "secondary": "#3B82F6", "text_primary": "#0F172A", "text_secondary": "#64748B",
        "chart_colors": ['#2563EB', '#10B981', '#F59E0B', '#6366F1', '#8B5CF6'],
        "plotly_template": "plotly_white"
    },
    "Enterprise Dark": {
        "bg": "#0B0F19", "card_bg": "#111827", "sidebar_bg": "#0F172A", "border": "#1F2937",
        "primary": "#3B82F6", "secondary": "#60A5FA", "text_primary": "#F9FAFB", "text_secondary": "#9CA3AF",
        "chart_colors": ['#3B82F6', '#10B981', '#FBBF24', '#818CF8', '#A78BFA'],
        "plotly_template": "plotly_dark"
    }
}

def apply_theme():
    # Injects custom CSS with universal adaptive colors
    t = THEMES[st.session_state.theme]
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Outfit', -apple-system, sans-serif !important;
    }}
    
    .stApp {{ background-color: {t['bg']}; }}

    /* 1. SMART ADAPTIVE TEXT */
    h1, h2, h3, h4, h5, h6, .stMarkdown p, .stMarkdown li, label, .st-emotion-cache-1wivap2 {{
        color: {t['text_primary']} !important;
    }}

    /* 2. SIDEBAR LOCKDOWN */
    [data-testid="stSidebar"] > div:first-child {{
        background-color: {t['sidebar_bg']} !important;
        border-right: 1px solid {t['border']} !important;
    }}
    
    /* Pull the sidebar content higher up */
    [data-testid="stSidebarUserContent"] {{
        padding-top: 1rem !important; 
    }}
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
        color: {t['text_primary']} !important;
    }}

    /* 3. BULLETPROOF INPUT BOXES */
    input, textarea, div[data-baseweb="select"] > div {{
        background-color: {t['card_bg']} !important;
        color: {t['text_primary']} !important;
        -webkit-text-fill-color: {t['text_primary']} !important;
        border: 2px solid {t['border']} !important;
        border-radius: 8px !important;
        transition: all 0.2s ease;
    }}
    
    div[data-baseweb="select"] input {{
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }}
    
    div[data-baseweb="select"] svg {{
        fill: {t['text_primary']} !important;
        color: {t['text_primary']} !important;
    }}
    
    input::placeholder, textarea::placeholder {{
        color: {t['text_secondary']} !important;
        -webkit-text-fill-color: {t['text_secondary']} !important;
        opacity: 0.7 !important;
    }}
    
    div[data-baseweb="select"] > div:hover, input:hover, input:focus {{
        border-color: {t['primary']} !important;
        box-shadow: 0 0 0 1px {t['primary']} !important;
    }}

    /* 4. BASE WEB POPOVERS */
    div[data-baseweb="popover"] > div, 
    div[data-baseweb="popover"] ul, 
    ul[data-baseweb="menu"], 
    ul[role="listbox"] {{
        background-color: {t['card_bg']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: 8px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
    }}
    
    li[role="option"] {{ 
        color: {t['text_primary']} !important; 
        background-color: transparent !important;
    }}
    
    li[role="option"]:hover, li[aria-selected="true"] {{ 
        background-color: {t['bg']} !important; 
        color: {t['primary']} !important; 
    }}

    /* Multiselect Tags */
    span[data-baseweb="tag"] {{
        background-color: {t['bg']} !important;
        color: {t['text_primary']} !important;
        border: 1px solid {t['border']} !important;
    }}
    span[data-baseweb="tag"] span {{
        color: {t['text_primary']} !important;
    }}

    /* 5. PAGE LOAD ANIMATIONS */
    @keyframes fadeSlideUp {{
        0% {{ opacity: 0; transform: translateY(30px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}

    div[data-testid="metric-container"], [data-testid="stPlotlyChart"], .stDataFrame, div[data-testid="stForm"] {{
        animation: fadeSlideUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}

    div[data-testid="metric-container"]:nth-child(1) {{ animation-delay: 0.1s; }}
    div[data-testid="metric-container"]:nth-child(2) {{ animation-delay: 0.2s; }}
    div[data-testid="metric-container"]:nth-child(3) {{ animation-delay: 0.3s; }}
    [data-testid="stPlotlyChart"] {{ animation-delay: 0.4s; }}

    /* 6. INTERACTIVE KPI CARDS & PHYSICS */
    div[data-testid="metric-container"] {{
        background: {t['card_bg']};
        border-radius: 20px;
        padding: 1.8rem;
        border: 1px solid {t['border']};
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); 
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
        position: relative;
    }}

    div[data-testid="metric-container"]:hover {{
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px {t['primary']}33; 
        border-color: {t['primary']};
    }}
    
    div[data-testid="stMetricValue"] {{
        font-weight: 800 !important;
        font-size: 2.4rem !important;
        background: -webkit-linear-gradient(45deg, {t['primary']}, {t['secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }}

    div[data-testid="stMetricLabel"] {{
        color: {t['text_secondary']} !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* 7. INTERACTIVE CHARTS */
    [data-testid="stPlotlyChart"] {{
        background-color: {t['card_bg']};
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        border: 1px solid {t['border']};
        padding: 1rem;
        box-sizing: border-box;
        transition: all 0.3s ease;
    }}

    [data-testid="stPlotlyChart"]:hover {{
        transform: translateY(-4px);
        box-shadow: 0 15px 35px {t['secondary']}22; 
    }}

    /* 8. TACTILE BUTTONS */
    div.stButton > button, div.stDownloadButton > button, div.stFormSubmitButton > button {{
        background: linear-gradient(135deg, {t['primary']}, {t['secondary']}) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px {t['primary']}40 !important;
        transform: scale(1);
    }}
    
    div.stButton > button *, div.stDownloadButton > button *, div.stFormSubmitButton > button * {{
        color: #ffffff !important; 
        -webkit-text-fill-color: #ffffff !important;
    }}
    
    div.stButton > button:hover, div.stDownloadButton > button:hover, div.stFormSubmitButton > button:hover {{
        transform: scale(1.05) translateY(-2px);
        box-shadow: 0 8px 25px {t['primary']}66 !important;
    }}
    
    div.stButton > button:active, div.stDownloadButton > button:active, div.stFormSubmitButton > button:active {{
        transform: scale(0.95) translateY(0); 
        box-shadow: 0 2px 10px {t['primary']}40 !important;
    }}

    /* 9. ANIMATED & TACTILE TABS */
    .stTabs [data-baseweb="tab-list"] {{ 
        gap: 0.5rem; 
        background-color: transparent; 
        border-bottom: 2px solid {t['border']}; 
        padding-top: 10px;
    }}
    
    .stTabs [data-baseweb="tab"] {{ 
        height: 3.2rem; 
        background-color: transparent; 
        color: {t['text_secondary']} !important; 
        font-weight: 600; 
        font-size: 1.1rem; 
        padding: 0 1.5rem;
        border-radius: 10px 10px 0 0;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        color: {t['text_primary']} !important;
        background-color: {t['card_bg']} !important;
        transform: translateY(-6px); 
        box-shadow: 0 -6px 15px rgba(0,0,0,0.08); 
    }}
    
    .stTabs [aria-selected="true"] {{ 
        color: {t['primary']} !important; 
        border-bottom: 3px solid {t['primary']} !important; 
        background-color: transparent !important;
    }}
    
    .stTabs [data-baseweb="tab-highlight"] {{ display: none; }}

   /* 10. FILE UPLOADER FIXES */
    [data-testid="stFileUploadDropzone"] {{
        background-color: {t['card_bg']} !important;
        border: 2px dashed {t['border']} !important;
        border-radius: 12px !important;
    }}
    
    [data-testid="stFileUploadDropzone"] * {{
        color: {t['text_primary']} !important;
    }}

    [data-testid="stUploadedFile"],
    div.stUploadedFile {{
        background-color: {t['bg']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: 8px !important;
    }}

    [data-testid="stUploadedFile"] *,
    div.stUploadedFile * {{
        background-color: transparent !important;
        color: {t['text_primary']} !important;
        fill: {t['text_primary']} !important;
        box-shadow: none !important;
    }}

    /* 11. TOP HEADER & LAYOUT FIXES */
    [data-testid="stHeader"] {{ 
        background-color: {t['bg']} !important; 
    }}
    #MainMenu, footer, .stDeployButton {{ display: none; }}
    .block-container {{ padding-top: 2rem !important; padding-bottom: 3rem !important; max-width: 1400px !important; }}
    
    /* 12. LOADING SPINNER FIX */
    [data-testid="stSpinner"] * {{
        color: {t['text_primary']} !important;
        stroke: {t['primary']} !important;
    }}
    </style>
    """, unsafe_allow_html=True)