import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io
import json
import os
import hashlib
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import jinja2
from streamlit_cookies_controller import CookieController

# ==========================================
# 1. THEME CONFIGURATIONS & STYLING
# ==========================================

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
    
    /* Removes the border from the hidden search box inside dropdowns */
    div[data-baseweb="select"] input {{
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }}
    
    /* Forces dropdown arrows to be visible on light themes */
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

    /* 9. ANIMATED TABS */
    .stTabs [data-baseweb="tab-list"] {{ gap: 2rem; background-color: transparent; border-bottom: 2px solid {t['border']}; }}
    .stTabs [data-baseweb="tab"] {{ 
        height: 3rem; background-color: transparent; 
        color: {t['text_secondary']} !important; font-weight: 600; font-size: 1.1rem; 
        padding-bottom: 0; transition: color 0.3s ease;
    }}
    .stTabs [aria-selected="true"] {{ color: {t['primary']} !important; border-bottom: 3px solid {t['primary']} !important; }}
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

    /* 🛑 THE ABSOLUTE OVERRIDE FOR THE FILE PILL */
    [data-testid="stUploadedFile"],
    div.stUploadedFile {{
        background-color: {t['bg']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: 8px !important;
    }}

    /* Nuke EVERY background color on EVERY child element inside the file box */
    [data-testid="stUploadedFile"] *,
    div.stUploadedFile * {{
        background-color: transparent !important;
        color: {t['text_primary']} !important;
        fill: {t['text_primary']} !important;
        box-shadow: none !important;
    }}

    /* 11. TOP HEADER & LAYOUT FIXES (Forces header to match theme) */
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

# ==========================================
# 2. DATA LOADING & PROCESSING
# ==========================================
@st.cache_data
def load_data(uploaded_file):
    # Loads CSV, Excel, JSON, or Parquet data and normalizes column names
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding="latin1")
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.json'):
            df = pd.read_json(uploaded_file)
        elif uploaded_file.name.endswith('.parquet'):
            df = pd.read_parquet(uploaded_file)
        else:
            st.error("Unsupported file format.")
            return None
            
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        
        if "order_date" in df.columns:
            df["order_date"] = pd.to_datetime(df["order_date"], errors='coerce')
            
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None
            

@st.cache_data
def generate_demo_data():
    """Generates 3 years of realistic synthetic sales data for testing."""
    np.random.seed(42)
    
    # Generate 3 years of dates
    dates = pd.date_range(start='2021-01-01', end='2023-12-31', freq='D').tolist() * 5
    
    regions = ['North America', 'EMEA', 'APAC', 'LATAM']
    categories = ['SaaS Subscriptions', 'Enterprise Hardware', 'Cloud Storage', 'Consulting']
    customers = [f'ENT-{i:04d}' for i in range(1, 150)]
    
    df = pd.DataFrame({
        'order_id': [f'ORD-{i:05d}' for i in range(1, len(dates) + 1)],
        'order_date': dates,
        'region': np.random.choice(regions, len(dates), p=[0.45, 0.30, 0.15, 0.10]),
        'category': np.random.choice(categories, len(dates)),
        'customer_id': np.random.choice(customers, len(dates)),
        'sales': np.random.normal(2500, 800, len(dates))
    })
    
    # Inject seasonal trends and year-over-year growth so Prophet looks good
    df['sales'] = df['sales'] + (df['order_date'].dt.month * 200) + ((df['order_date'].dt.year - 2021) * 1500)
    
    # Inject a couple of massive anomalies for Scikit-Learn to catch
    anomaly_indices = np.random.choice(df.index, size=10, replace=False)
    df.loc[anomaly_indices, 'sales'] = df.loc[anomaly_indices, 'sales'] * np.random.uniform(4, 8, size=10)
    
    df['sales'] = df['sales'].clip(lower=100).round(2)
    df['profit'] = (df['sales'] * np.random.uniform(0.15, 0.45, len(dates))).round(2)
    
    return df

# ==========================================
# 3. SIDEBAR CONTROLS & FILTERS
# ==========================================
def render_sidebar(df):
    # Renders the sidebar global data filters
    st.sidebar.title("🎨 Theme Settings")
    selected_theme = st.sidebar.selectbox("Select Theme", options=list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.theme))
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        # Save it to the database so it remembers for next time!
        if 'logged_in' in st.session_state and st.session_state.logged_in:
            update_user_theme(st.session_state.current_user, selected_theme)
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.title("🔍 Global Filters")
    st.sidebar.markdown("Filter your data across all tabs.")
    
    filtered_df = df.copy()
    
    if "order_date" in filtered_df.columns:
        valid_dates = filtered_df["order_date"].dropna()
        if not valid_dates.empty:
            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()
            date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
            if len(date_range) == 2:
                start_date, end_date = date_range
                filtered_df = filtered_df[
                    (filtered_df["order_date"].dt.date >= start_date) & 
                    (filtered_df["order_date"].dt.date <= end_date)
                ]
    
    if "region" in filtered_df.columns:
        regions = st.sidebar.multiselect("Select Region", options=sorted(df["region"].dropna().unique()))
        if regions:
            filtered_df = filtered_df[filtered_df["region"].isin(regions)]
            
    if "category" in filtered_df.columns:
        categories = st.sidebar.multiselect("Select Category", options=sorted(df["category"].dropna().unique()))
        if categories:
            filtered_df = filtered_df[filtered_df["category"].isin(categories)]
            
    return filtered_df

# ==========================================
# 4. DASHBOARD VIEW (KPIs & Charts)
# ==========================================
def render_dashboard(df):
    # Renders the main executive dashboard with metrics and visual charts
    st.header("Executive Sales Dashboard")
    t = THEMES[st.session_state.theme]
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    st.markdown("### Key Performance Indicators")
    total_sales = df["sales"].sum() if "sales" in df.columns else 0
    total_orders = df["order_id"].nunique() if "order_id" in df.columns else len(df)
    
    # SMART MIDDLE KPI: Profit -> Avg Order Value -> Units Sold
    if "profit" in df.columns:
        mid_label = "Total Profit"
        mid_val = f"${df['profit'].sum():,.2f}"
    elif "sales" in df.columns and total_orders > 0:
        mid_label = "Avg Order Value"
        mid_val = f"${(total_sales / total_orders):,.2f}"
    elif "quantity" in df.columns:
        mid_label = "Total Units Sold"
        mid_val = f"{int(df['quantity'].sum()):,}"
    else:
        mid_label = "Avg Value per Row"
        mid_val = f"${(total_sales / len(df)) if len(df) > 0 else 0:,.2f}"
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric(mid_label, mid_val)
    col3.metric("Total Orders", f"{total_orders:,}")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # ... Your chart code starts below this line (row1_col1, row1_col2 = st.columns...)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    row1_col1, row1_col2 = st.columns((2, 1), gap="large") 
    
    with row1_col1:
        if "order_date" in df.columns and "sales" in df.columns:
            st.subheader("Monthly Sales Trend")
            trend_df = df.dropna(subset=['order_date']).copy()
            sales_trend = trend_df.groupby(trend_df['order_date'].dt.to_period('M'))['sales'].sum().reset_index()
            sales_trend['order_date'] = sales_trend['order_date'].dt.to_timestamp()
            
            fig_trend = px.area(
                sales_trend, x="order_date", y="sales",
                color_discrete_sequence=[THEMES[st.session_state.theme]['primary']],
                template=THEMES[st.session_state.theme]['plotly_template']
            )
            fig_trend.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=40, b=20),
                xaxis_title="", yaxis_title="Sales ($)",
                xaxis=dict(showgrid=False, color=t['text_secondary'], tickfont=dict(color=t['text_secondary'])),
                yaxis=dict(showgrid=True, gridcolor=t['border'], color=t['text_secondary'], tickfont=dict(color=t['text_secondary']))
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
    with row1_col2:
        if "category" in df.columns and "sales" in df.columns:
            st.subheader("Sales by Category")
            sales_cat = df.groupby("category")["sales"].sum().reset_index()
            fig_cat = px.pie(
                sales_cat, names="category", values="sales", hole=0.5,
                color_discrete_sequence=THEMES[st.session_state.theme]['chart_colors'],
                template=THEMES[st.session_state.theme]['plotly_template']
            )
            fig_cat.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40, r=40, t=40, b=80), 
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, font=dict(color=t['text_secondary']))
            )
            fig_cat.update_traces(textposition='inside', textinfo='percent', hoverinfo='label+percent+value')
            st.plotly_chart(fig_cat, use_container_width=True)
            
    row2_col1, row2_col2 = st.columns(2, gap="large")
    
    st.markdown("---")
    st.subheader("⚠️ AI Anomaly Detection")
    if "order_date" in df.columns and "sales" in df.columns:
        from sklearn.ensemble import IsolationForest
        
        # Prepare daily data
        daily_anom = df.groupby(df['order_date'].dt.date)['sales'].sum().reset_index()
        daily_anom['order_date'] = pd.to_datetime(daily_anom['order_date'])
        
        if len(daily_anom) > 20:
            # Train Isolation Forest
            iso = IsolationForest(contamination=0.05, random_state=42)
            daily_anom['anomaly'] = iso.fit_predict(daily_anom[['sales']])
            
            # Filter the anomalies (-1 means anomalous)
            anomalies = daily_anom[daily_anom['anomaly'] == -1]
            
            if not anomalies.empty:
                st.warning(f"**System Alert:** Detected {len(anomalies)} irregular sales days that deviate from normal patterns.")
                
                # Plot anomalies over the normal line
                fig_anom = px.line(daily_anom, x='order_date', y='sales', template=t['plotly_template'])
                fig_anom.update_traces(line_color=t['text_secondary'], opacity=0.5)
                
                fig_anom.add_scatter(x=anomalies['order_date'], y=anomalies['sales'], 
                                     mode='markers', marker=dict(color='#ef4444', size=10, symbol='x'), 
                                     name='Anomalies')
                
                fig_anom.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20),
                                       plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_anom, use_container_width=True)
            else:
                st.success("System Status: Normal. No extreme sales anomalies detected in the selected date range.")
    
    with row2_col1:
        if "region" in df.columns and "sales" in df.columns:
            st.subheader("Regional Performance")
            sales_region = df.groupby("region")["sales"].sum().reset_index().sort_values("sales", ascending=True)
            fig_region = px.bar(
                sales_region, y="region", x="sales", orientation='h',
                color_discrete_sequence=[THEMES[st.session_state.theme]['primary']],
                template=THEMES[st.session_state.theme]['plotly_template']
            )
            fig_region.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=40, b=20), coloraxis_showscale=False,
                xaxis_title="Sales ($)", yaxis_title="",
                xaxis=dict(showgrid=True, gridcolor=t['border'], color=t['text_secondary'], tickfont=dict(color=t['text_secondary'])),
                yaxis=dict(showgrid=False, color=t['text_secondary'], tickfont=dict(color=t['text_secondary']))
            )
            st.plotly_chart(fig_region, use_container_width=True)
            
    with row2_col2:
        prod_col = "product_name" if "product_name" in df.columns else "product" if "product" in df.columns else None
        if prod_col and "sales" in df.columns:
            st.subheader("Top 10 Selling Products")
            top_products = df.groupby(prod_col)["sales"].sum().reset_index().sort_values("sales", ascending=True).tail(10)
            fig_top = px.bar(
                top_products, y=prod_col, x="sales", orientation='h',
                color_discrete_sequence=[THEMES[st.session_state.theme]['secondary']],
                template=THEMES[st.session_state.theme]['plotly_template']
            )
            fig_top.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=40, b=20), coloraxis_showscale=False,
                xaxis_title="Sales ($)", yaxis_title="",
                xaxis=dict(showgrid=True, gridcolor=t['border'], color=t['text_secondary'], tickfont=dict(color=t['text_secondary'])),
                yaxis=dict(showgrid=False, color=t['text_secondary'], tickfont=dict(color=t['text_secondary']))
            )
            fig_top.update_yaxes(ticktext=[f"{str(name)[:30]}..." if len(str(name)) > 30 else name for name in top_products[prod_col]], 
                                 tickvals=top_products[prod_col])
            st.plotly_chart(fig_top, use_container_width=True)

# ==========================================
# 5. DATA VIEW (Raw Data Table)
# ==========================================
def render_data_view(df):
    # Renders the raw interactive dataset view and download capabilities
    st.header("Dataset Details & Reports")
    st.write(f"Showing **{len(df):,}** rows based on current filters.")
    
    col1, col2 = st.columns(2)
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Report (CSV)",
            data=csv,
            file_name='sales_report.csv',
            mime='text/csv',
            use_container_width=True
        )
    with col2:
        total_sales = float(df['sales'].sum()) if 'sales' in df.columns else 0.0
        orders = int(df['order_id'].nunique()) if 'order_id' in df.columns else len(df)
        
        sales_str = "${:,.2f}".format(total_sales)
        orders_str = "{:,}".format(orders)
        rows_str = "{:,}".format(len(df))
        
        # HTML built safely without triple quotes
        html_content = (
            "<html>\n"
            "<head><title>Executive Sales Report</title></head>\n"
            "<body style=\"font-family: 'Outfit', -apple-system, sans-serif; padding: 20px;\">\n"
            "    <h2>Executive Sales Summary Report</h2>\n"
            "    <p>Generated automatically by the AI Sales Dashboard.</p>\n"
            "    <hr>\n"
            "    <h3>Key Metrics</h3>\n"
            "    <ul>\n"
            f"        <li><b>Total Sales:</b> {sales_str}</li>\n"
            f"        <li><b>Total Orders:</b> {orders_str}</li>\n"
            f"        <li><b>Dataset Rows Analyzed:</b> {rows_str}</li>\n"
            "    </ul>\n"
            "    <p><i>More detailed AI insights can be viewed live on the dashboard platform.</i></p>\n"
            "</body>\n"
            "</html>"
        )
        
        st.download_button(
            label="📄 Download Executive Report (HTML)",
            data=html_content,
            file_name='executive_summary.html',
            mime='text/html',
            use_container_width=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    t = THEMES[st.session_state.theme]
    
    styled_df = df.style.set_properties(**{
        'background-color': t['card_bg'],
        'color': t['text_primary'],
        'border-color': t['border']
    })
    st.dataframe(styled_df, use_container_width=True)

# ==========================================
# 6. AI & BUSINESS INSIGHTS
# ==========================================
def render_insights(df):
    # Generates dynamic business insights using the Gemini LLM API
    st.header("🧠 Generative AI Business Insights")
    st.markdown("Actionable, data-driven recommendations analyzed in real-time by Google Gemini.")
    
    if df.empty:
        st.warning("Not enough data to generate insights.")
        return

    st.markdown("---")
    
    import os
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            pass
            
    if 'gemini_api_key' in st.session_state and st.session_state.gemini_api_key:
        api_key = st.session_state.gemini_api_key

    if not api_key:
        st.warning("⚠️ **Gemini API Key Required**")
        st.info("To unlock real-time generative insights, please go to the '💬 Chat AI' tab and enter your API Key first.")
        return

    if st.button("✨ Generate Custom AI Insights", use_container_width=True):
        with st.spinner("Analyzing dataset patterns... this takes a few seconds."):
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                
                model = genai.GenerativeModel('gemini-2.5-flash') 
                
                summary_stats = df.describe(include='all').to_string()
                
                prompt = (
                    "You are an expert Chief Revenue Officer and Data Scientist analyzing a corporate sales dataset.\n"
                    "Here is the statistical summary of the dataset:\n\n"
                    f"{summary_stats}\n\n"
                    "Based STRICTLY on these numbers, provide 4 highly actionable, distinct business insights.\n"
                    "Format your response with clean Markdown. Use emojis, headings, bullet points, and highlight key numbers in bold.\n"
                    "Do not use generic advice; tie everything to the specific data provided above.\n"
                    "Categorize them clearly into two sections: Performance & Trends and Portfolio & Behavior."
                )
                
                response = model.generate_content(prompt)
                
                st.success("Analysis Complete!")
                
                t = THEMES[st.session_state.theme]
                card_bg = t['card_bg']
                card_border = t['border']
                response_text = response.text
                
                html_block = (
                    f'<div style="background-color: {card_bg}; '
                    f'padding: 2rem; '
                    f'border-radius: 12px; '
                    f'border: 1px solid {card_border};">'
                    f'{response_text}'
                    f'</div>'
                )
                
                st.markdown(html_block, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Failed to generate insights. Error details: {e}")

# ==========================================
# 7. FORECASTING & MACHINE LEARNING (PROPHET)
# ==========================================
def render_forecasting(df):
    st.header("📈 Predictive Sales Forecasting")
    st.markdown("Utilizing Prophet time-series modeling to project 30-day performance based on weekly seasonality and historical trends.")
    
    if "order_date" not in df.columns or "sales" not in df.columns:
        st.warning("Forecasting requires 'order_date' and 'sales' columns.")
        return
        
    # Prepare data for Prophet (requires columns named 'ds' and 'y')
    daily_sales = df.groupby(df['order_date'].dt.date)['sales'].sum().reset_index()
    daily_sales.columns = ['ds', 'y']
    daily_sales['ds'] = pd.to_datetime(daily_sales['ds'])
    daily_sales = daily_sales.sort_values('ds')
    
    if len(daily_sales) < 30:
        st.warning("Not enough historical data for a reliable ML forecast (minimum 30 days required).")
        return
        
    with st.spinner("Training Prophet time-series model..."):
        from prophet import Prophet
        
        # Initialize and train the model
        m = Prophet(yearly_seasonality=False, daily_seasonality=False)
        m.fit(daily_sales)
        
        # Predict the next 30 days
        future = m.make_future_dataframe(periods=30)
        forecast = m.predict(future)
        
        # Setup the plot
        import plotly.graph_objects as go
        fig = go.Figure()
        t = THEMES[st.session_state.theme]
        
        # Historical Data
        fig.add_trace(go.Scatter(x=daily_sales['ds'], y=daily_sales['y'], mode='markers', name='Actual Sales', marker=dict(color=t['primary'], size=6, opacity=0.5)))
        
        # Prophet Trend Line
        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Prophet Forecast', line=dict(color=t['secondary'], width=3)))
        
        # Confidence Intervals
        fig.add_trace(go.Scatter(
            x=pd.concat([forecast['ds'], forecast['ds'][::-1]]),
            y=pd.concat([forecast['yhat_upper'], forecast['yhat_lower'][::-1]]),
            fill='toself', fillcolor=t['primary'], opacity=0.1,
            line=dict(color='rgba(255,255,255,0)'), hoverinfo="skip", showlegend=False, name='Confidence Interval'
        ))
        
        fig.update_layout(
            template=t['plotly_template'], 
            height=450, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=50, t=60, b=80), font=dict(color=t['text_secondary']), 
            
            # 🛠️ THE FIX: Explicitly setting the font color inside the legend
            legend=dict(
                orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5,
                font=dict(color=t['text_primary']) 
            ),
            
            xaxis=dict(
                showgrid=False, showline=True, linecolor=t['border'], linewidth=1, 
                color=t['text_secondary'], tickfont=dict(color=t['text_secondary']) 
            ),
            yaxis=dict(
                showgrid=True, gridcolor=t['border'], showline=True, linecolor=t['border'], linewidth=1, 
                color=t['text_secondary'], tickfont=dict(color=t['text_secondary']) 
            )
        )

        st.plotly_chart(fig, use_container_width=True)
        
        future_val = forecast.iloc[-1]['yhat']
        st.info(f"**ML Projection Insight**: Based on detected seasonal patterns and historical trends, the model projects sales to normalize around **${future_val:,.2f}** per day by the end of the next 30-day cycle.")

# ==========================================
# 8. CUSTOMER RISK & RFM ANALYSIS
# ==========================================
def render_rfm_analysis(df):
    st.header("⚠️ Customer Risk & RFM Analysis")
    st.markdown("Identifies high-value customers who are at risk of churning based on Recency, Frequency, and Monetary value.")
    
    customer_col = next((col for col in ['customer_id', 'customer_name', 'customer'] if col in df.columns), None)
            
    if not customer_col or "order_date" not in df.columns or "sales" not in df.columns:
        st.warning("RFM Analysis requires Customer ID/Name, Order Date, and Sales columns.")
        return
        
    current_date = df['order_date'].max()
    
    freq_col = 'order_id' if 'order_id' in df.columns else 'sales'
    freq_agg = 'nunique' if 'order_id' in df.columns else 'count'
    
    rfm = df.groupby(customer_col).agg(
        Recency=('order_date', lambda x: (current_date - x.max()).days),
        Frequency=(freq_col, freq_agg),
        Monetary=('sales', 'sum')
    ).reset_index()
    
    rfm.rename(columns={'Recency': 'Recency (Days)', 'Monetary': 'Total Spend ($)'}, inplace=True)
    
    quantiles = rfm[['Recency (Days)', 'Frequency', 'Total Spend ($)']].quantile(q=[0.33, 0.66])
    
    def r_score(x):
        if x <= quantiles['Recency (Days)'][0.33]: return 3 
        elif x <= quantiles['Recency (Days)'][0.66]: return 2
        else: return 1 
        
    def fm_score(x, c):
        if x <= quantiles[c][0.33]: return 1
        elif x <= quantiles[c][0.66]: return 2
        else: return 3
        
    rfm['R'] = rfm['Recency (Days)'].apply(r_score)
    rfm['F'] = rfm['Frequency'].apply(fm_score, args=('Frequency',))
    rfm['M'] = rfm['Total Spend ($)'].apply(fm_score, args=('Total Spend ($)',))
    
    at_risk = rfm[(rfm['R'] == 1) & (rfm['M'] >= 2)]
    num_at_risk = len(at_risk)
    total_customers = len(rfm)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if num_at_risk == 0:
            st.success("✅ **System Status: Optimal**\n\nEverything looks good! You currently have **0** high-value customers at risk of churning. Your retention strategies are working perfectly.")
        else:
            # Calculate risk severity and revenue at risk
            risk_pct = num_at_risk / total_customers if total_customers > 0 else 0
            revenue_at_risk = at_risk['Total Spend ($)'].sum()
            
            if risk_pct < 0.05:
                # Less than 5% of customers at risk
                st.warning(f"🟡 **Low Risk Detected**\nYou have **{num_at_risk}** high-value customers showing early signs of churn. Total revenue at risk: **${revenue_at_risk:,.2f}**.")
                st.markdown("**Action Plan:** Send a personalized 'We miss you' email with a small discount code to re-engage them before they drop off entirely.")
            
            elif risk_pct < 0.15:
                # 5% to 15% of customers at risk
                st.error(f"🟠 **Intermediate Risk Detected**\nYou have **{num_at_risk}** high-value customers at risk of churning. Total revenue at risk: **${revenue_at_risk:,.2f}**.")
                st.markdown("**Action Plan:** Trigger an automated win-back campaign. Offer a loyalty bonus or an exclusive perk on their next order to incentivize an immediate purchase.")
            
            else:
                # More than 15% of customers at risk
                st.error(f"🔴 **High Risk Detected (CRITICAL)**\nYou have **{num_at_risk}** high-value customers on the verge of churning. Total revenue at risk: **${revenue_at_risk:,.2f}**.")
                st.markdown("**Action Plan:** Immediate manual intervention required. Have an account manager contact these top accounts directly to gather feedback and offer a custom retention package.")
            
            # Display the data table only if there are actually at-risk customers
            t = THEMES[st.session_state.theme]
            rfm_display = at_risk.sort_values('Total Spend ($)', ascending=False).head(10)
            styled_rfm = rfm_display.style.set_properties(**{
                'background-color': t['card_bg'],
                'color': t['text_primary'],
                'border-color': t['border']
            })
            st.dataframe(styled_rfm, use_container_width=True)
        
    with col2:
        fig = px.scatter(rfm, x='Recency (Days)', y='Total Spend ($)', color='R', 
                         hover_name=customer_col, size='Frequency',
                         title="Recency vs Spend (Color: Recency Score)",
                         color_continuous_scale="RdYlGn")
        t = THEMES[st.session_state.theme] 
        
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20),
            font=dict(color=t['text_secondary']), 
            xaxis=dict(showgrid=False, color=t['text_secondary'], tickfont=dict(color=t['text_secondary'])),
            yaxis=dict(showgrid=True, gridcolor=t['border'], color=t['text_secondary'], tickfont=dict(color=t['text_secondary'])),
            coloraxis_colorbar=dict(
                title_font=dict(color=t['text_secondary']),
                tickfont=dict(color=t['text_secondary'])
            )
        )
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 9. GENERATIVE AI: CHAT WITH DATA
# ==========================================
def render_chat_data(df):
    st.header("💬 Chat with Your Data (AI Assistant)")
    st.markdown("Ask questions in plain English to instantly query your dataset. *(Powered by Google Gemini)*")
    
    import os
    
    if "gemini_api_key" not in st.session_state:
        st.session_state.gemini_api_key = ""

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            pass
            
    if not api_key:
        api_key = st.session_state.gemini_api_key
    
    if not api_key:
        st.warning("⚠️ **API Key Required**")
        
        api_message = (
            "To enable real AI responses, please provide a free Google Gemini API Key:\n"
            "1. Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)\n"
            "2. Enter it below to activate the assistant for this session:"
        )
        st.markdown(api_message)
        
        user_api_key = st.text_input("Enter Gemini API Key:", type="password")
        if user_api_key:
            st.session_state.gemini_api_key = user_api_key
            st.rerun()
        else:
            return

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error(f"Error initializing AI: {e}. Make sure `google-generativeai` is installed.")
        return
        
    user_query = st.text_input("Ask a question about your sales data:", placeholder="e.g., What do you suggest me to do differently to increase my profits?")
    
    if user_query:
        with st.spinner("Analyzing data and generating response..."):
            try:
                cols_str = ', '.join(df.columns)
                rows_len = len(df)
                stats_str = df.describe().to_string()
                head_str = df.head(3).to_string()
                
                context = (
                    "Here is a summary of the sales dataset:\n"
                    f"Columns: {cols_str}\n"
                    f"Number of rows: {rows_len}\n\n"
                    "Summary statistics:\n"
                    f"{stats_str}\n\n"
                    "Top 3 rows of data:\n"
                    f"{head_str}\n\n"
                    "Based on this specific data, answer the user question. Be concise, professional, and reference specific numbers from the dataset if applicable."
                )
                
                response = model.generate_content(f"{context}\n\nUser Question: {user_query}")
                
                st.success("AI Response:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error generating response: {e}. (Make sure your API key is valid).")

# ==========================================
# 9.5. ADVANCED AUTHENTICATION SYSTEM
# ==========================================
def init_db():
    conn = sqlite3.connect('dashboard_enterprise.db')
    c = conn.cursor()
    # Create user table with a dedicated column for their saved theme
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            saved_theme TEXT DEFAULT 'Neon Cyberpunk'
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database when the app runs
init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_user(email_or_phone, password):
    try:
        conn = sqlite3.connect('dashboard_enterprise.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", 
                  (email_or_phone, hash_password(password)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False # User already exists

def authenticate(email_or_phone, password):
    conn = sqlite3.connect('dashboard_enterprise.db')
    c = conn.cursor()
    c.execute("SELECT password, saved_theme FROM users WHERE email=?", (email_or_phone,))
    result = c.fetchone()
    conn.close()
    
    if result and result[0] == hash_password(password):
        # Load their saved theme into the session state!
        st.session_state.theme = result[1] 
        return True
    return False

def reset_password(email_or_phone, new_password):
    conn = sqlite3.connect('dashboard_enterprise.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password=? WHERE email=?", 
              (hash_password(new_password), email_or_phone))
    rows_affected = c.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def update_user_theme(email_or_phone, new_theme):
    if email_or_phone:
        conn = sqlite3.connect('dashboard_enterprise.db')
        c = conn.cursor()
        c.execute("UPDATE users SET saved_theme=? WHERE email=?", (new_theme, email_or_phone))
        conn.commit()
        conn.close()

def send_reset_email(target_email, otp_code):
    # ⚠️ IMPORTANT: Replace these with your actual email details
    sender_email = "aadiakarsh@gmail.com" 
    # Must be a 16-digit Google App Password, NOT your normal Gmail password!
    sender_password = "ufqf plte dtwd xphf" 

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = target_email
    msg['Subject'] = "AI Dashboard - Password Reset Code"

    body = f"Your secure password reset code is: {otp_code}\n\nIf you did not request this, please ignore this email."
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False

def render_login(controller):
    st.markdown("<h1 style='text-align: center; margin-top: 5rem;'>🔐 AI Sales Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Secure enterprise portal access.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        # Reduced to just 2 standard tabs
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                st.markdown("### Account Login")
                email_or_phone = st.text_input("Email or Mobile Number")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", use_container_width=True)
                
                if submit:
                    if authenticate(email_or_phone, password):
                        st.session_state.logged_in = True
                        st.session_state.current_user = email_or_phone
                        controller.set('logged_in_user', email_or_phone, max_age=86400)
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
            
            # 🛠️ THE FIX: Forgotten Password is now an expander inside the Login tab
            # 🛠️ THE REAL EMAIL FLOW
            with st.expander("Forgotten Password?"):
                if 'reset_step' not in st.session_state:
                    st.session_state.reset_step = 'request_code'
                
                # STEP 1: Request the code & Send Email
                if st.session_state.reset_step == 'request_code':
                    reset_user = st.text_input("Enter your registered Email", key="reset_user_input")
                    if st.button("Send Confirmation Code", use_container_width=True):
                        # Query SQLite to check if user exists
                        conn = sqlite3.connect('dashboard_enterprise.db')
                        c = conn.cursor()
                        c.execute("SELECT email FROM users WHERE email=?", (reset_user,))
                        user_exists = c.fetchone()
                        conn.close()
                        
                        if user_exists:
                            with st.spinner("Sending email..."):
                                generated_otp = str(random.randint(100000, 999999))
                                
                                # Call our new email function!
                                if send_reset_email(reset_user, generated_otp):
                                    st.session_state.reset_otp = generated_otp
                                    st.session_state.reset_target_user = reset_user
                                    st.session_state.reset_step = 'verify_code'
                                    st.rerun()
                                else:
                                    st.error("Failed to send email. Check server settings.")
                        else:
                            st.error("Account not found.")
                
                # STEP 2: Verify code and set new password
                elif st.session_state.reset_step == 'verify_code':
                    st.success(f"📧 A confirmation code has been sent to {st.session_state.reset_target_user}!")
                    
                    entered_code = st.text_input("Enter 6-digit Confirmation Code", key="reset_code_input")
                    new_reset_pass = st.text_input("New Password", type="password", key="reset_new_pass")
                    confirm_reset_pass = st.text_input("Confirm New Password", type="password", key="reset_confirm_pass")
                    
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("Cancel", use_container_width=True):
                            st.session_state.reset_step = 'request_code'
                            st.rerun()
                    with btn_col2:
                        if st.button("Verify & Update", use_container_width=True):
                            if entered_code != st.session_state.reset_otp:
                                st.error("Invalid confirmation code.")
                            elif new_reset_pass != confirm_reset_pass:
                                st.error("Passwords do not match.")
                            elif len(new_reset_pass) < 6:
                                st.error("Password must be at least 6 characters.")
                            else:
                                if reset_password(st.session_state.reset_target_user, new_reset_pass):
                                    st.success("Password updated! You can now log in.")
                                    st.session_state.reset_step = 'request_code'
                                else:
                                    st.error("An error occurred.")
                        
        with tab2:
            with st.form("signup_form"):
                st.markdown("### Create an Account")
                new_email_or_phone = st.text_input("Email or Mobile Number", key="signup_user")
                new_password = st.text_input("Password", type="password", key="signup_pass")
                confirm_password = st.text_input("Confirm Password", type="password")
                signup_submit = st.form_submit_button("Sign Up", use_container_width=True)
                
                if signup_submit:
                    if new_password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters.")
                    elif not new_email_or_phone:
                        st.error("Please enter a valid identifier.")
                    else:
                        if save_user(new_email_or_phone, new_password):
                            st.success("Account created successfully! Switch to the Login tab.")
                        else:
                            st.error("Account already exists.")

# ==========================================
# 10. MAIN APPLICATION ROUTER
# ==========================================
import time

def main():
    st.set_page_config(
        page_title="AI-Powered Sales Dashboard",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    controller = CookieController()
    
    time.sleep(0.3) 
    
    if 'theme' not in st.session_state or st.session_state.theme not in THEMES:
        st.session_state.theme = "Neon Cyberpunk"
        
    saved_user = controller.get('logged_in_user')
    if saved_user:
        st.session_state.logged_in = True
        st.session_state.current_user = saved_user
        
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.current_user = None
        
    apply_theme()
    
    if not st.session_state.logged_in:
        render_login(controller)
        return
        
    st.sidebar.markdown(f"Logged in as: **{st.session_state.current_user}**")
    if st.sidebar.button("Logout", use_container_width=True):
        controller.remove('logged_in_user')
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
    st.sidebar.markdown("---")
    
    st.sidebar.title("📂 Data Upload")
    
    # We remove the negative margin and use Streamlit's built-in label collapsing for a clean UI
    st.sidebar.markdown("**Upload Data File**")
    st.sidebar.markdown("<p style='font-size: 0.85rem; color: #9CA3AF;'>Supported: CSV, XLSX, XLS, JSON, PARQUET</p>", unsafe_allow_html=True)
    
    uploaded_file = st.sidebar.file_uploader(
        "Upload", 
        type=["csv", "xlsx", "xls", "json", "parquet"], 
        label_visibility="collapsed"
    )
    # Initialize demo state if it doesn't exist
    if 'use_demo' not in st.session_state:
        st.session_state.use_demo = False

    # If user uploads a real file, instantly turn off demo mode
    if uploaded_file is not None:
        st.session_state.use_demo = False

    # ROUTE 1: SHOW LANDING PAGE (No file, No Demo)
    if uploaded_file is None and not st.session_state.use_demo:
        st.sidebar.markdown("---")
        
        # 1. QUICK START DEMO
        st.sidebar.title("🚀 Quick Start")
        st.sidebar.markdown("<p style='font-size: 0.85rem; color: #94a3b8;'>Don't have a dataset ready? Test the engine with our dummy data.</p>", unsafe_allow_html=True)
        if st.sidebar.button("Load Enterprise Demo Data", use_container_width=True):
            st.session_state.use_demo = True
            st.rerun() 
            
        st.sidebar.markdown("---")
        
        # 2. SYSTEM HEALTH
        st.sidebar.title("📡 System Status")
        st.sidebar.markdown("""
        <div style="font-size: 0.9rem; color: #a1a1aa;">
            <span style="color: #10b981;">●</span> Secure SQLite Auth<br>
            <span style="color: #10b981;">●</span> Prophet ML Engine<br>
            <span style="color: #10b981;">●</span> Gemini LLM Ready
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown("---")
        
        # 3. UPLOAD GUIDELINES
        with st.sidebar.expander("📊 CSV Formatting Guide"):
            st.markdown("""
            <div style="font-size: 0.85rem; color: #a1a1aa;">
            For optimal AI analysis, include these columns:<br><br>
            • <code>order_date</code> (Dates)<br>
            • <code>sales</code> (Numbers)<br>
            • <code>profit</code> (Numbers)<br>
            • <code>region</code> (Text)<br>
            • <code>category</code> (Text)<br>
            • <code>customer_id</code> (Text/Numbers)
            </div>
            """, unsafe_allow_html=True)

        # ==========================================
        # 🚀 PREMIUM VERCEL/STRIPE-STYLE LANDING PAGE
        # ==========================================
        st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&display=swap');
.stApp {
background-color: #030305 !important;
background-image: radial-gradient(circle at 15% 50%, rgba(87, 115, 255, 0.12), transparent 25%), radial-gradient(circle at 85% 30%, rgba(0, 240, 255, 0.12), transparent 25%), linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px) !important;
background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px !important;
background-position: 0 0, 0 0, -1px -1px, -1px -1px !important;
}
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 1rem !important; max-width: 1200px !important; }
[data-testid="stSidebar"] {
background: rgba(10, 10, 15, 0.6) !important;
backdrop-filter: blur(20px) !important;
-webkit-backdrop-filter: blur(20px) !important;
border-right: 1px solid rgba(255,255,255,0.05) !important;
}
[data-testid="stSidebarUserContent"] { padding-top: 3rem; }
.hero-wrapper {
text-align: center; padding: 4rem 1rem 3rem 1rem;
animation: fadeSlideUp 1s cubic-bezier(0.16, 1, 0.3, 1); font-family: 'Inter', sans-serif;
}
.hero-title {
font-family: 'Space Grotesk', sans-serif; font-size: clamp(3rem, 5vw, 4.5rem);
font-weight: 800; line-height: 1.1; margin-bottom: 1.5rem; color: #ffffff; letter-spacing: -1px;
}
.text-glow {
background: linear-gradient(to right, #00F0FF, #5773FF, #FF007A);
-webkit-background-clip: text; -webkit-text-fill-color: transparent;
background-size: 200% auto; animation: gradientMove 5s linear infinite;
}
.hero-subtitle {
font-size: 1.25rem; color: #94a3b8; max-width: 600px; margin: 0 auto 2rem auto; line-height: 1.6;
}
.about-platform-box {
background: rgba(255, 255, 255, 0.02);
border: 1px solid rgba(255, 255, 255, 0.05);
border-left: 4px solid #00F0FF;
border-radius: 12px;
padding: 2rem;
max-width: 800px;
margin: 0 auto 4rem auto;
text-align: left;
backdrop-filter: blur(20px);
-webkit-backdrop-filter: blur(20px);
}
.about-platform-box h3 {
font-family: 'Space Grotesk', sans-serif; color: #f8fafc; margin-top: 0; margin-bottom: 1rem; font-size: 1.5rem;
}
.about-platform-box p {
color: #94a3b8; font-size: 1.05rem; line-height: 1.7; margin: 0;
}
.feature-grid {
display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; text-align: left; margin-bottom: 3rem;
}
.feature-card {
background: rgba(15, 15, 20, 0.4); border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 16px; padding: 2rem; transition: all 0.3s ease;
}
.feature-card:hover {
background: rgba(30, 30, 40, 0.4); border-color: rgba(255, 255, 255, 0.1); transform: scale(1.02);
}
.feature-icon {
font-size: 1.5rem; margin-bottom: 1rem; display: inline-flex; align-items: center; justify-content: center;
width: 48px; height: 48px; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px;
}
.feature-title { font-family: 'Space Grotesk'; font-size: 1.25rem; font-weight: 600; color: #f1f5f9; margin-bottom: 0.5rem; }
.feature-desc { color: #94a3b8; font-size: 0.95rem; line-height: 1.6; }
@keyframes fadeSlideUp { 0% { opacity: 0; transform: translateY(30px); } 100% { opacity: 1; transform: translateY(0); } }
@keyframes gradientMove { 0% { background-position: 0% center; } 100% { background-position: 200% center; } }
</style>
<div class="hero-wrapper">
<h1 class="hero-title">
Next-Gen <span class="text-glow">Sales Intelligence</span>
</h1>
<p class="hero-subtitle">
Upload your raw datasets and let autonomous AI uncover hidden revenue streams, predict market trends, and instantly generate enterprise-grade reports.
</p>
<div class="about-platform-box" style="animation: fadeSlideUp 0.8s ease 0.1s both;">
<h3>About This Platform</h3>
<p>
This dashboard is a fully integrated data science environment built to transform raw CSV and Excel files into actionable business intelligence. It securely processes your data locally, utilizing advanced machine learning pipelines like <strong>Facebook Prophet</strong> for time-series forecasting and <strong>Scikit-Learn Isolation Forests</strong> for real-time anomaly detection. Integrated with Google's <strong>Gemini LLM</strong>, it serves as an autonomous data analyst, capable of generating executive summaries and answering natural language queries about your datasets instantly.
</p>
</div>
<div class="feature-grid">
<div class="feature-card" style="animation: fadeSlideUp 0.8s ease 0.3s both;"><div class="feature-icon">🧠</div><div class="feature-title">Generative AI Insights</div><div class="feature-desc">Google Gemini analyzes your raw CSVs in real-time to output actionable, C-suite level executive summaries.</div></div>
<div class="feature-card" style="animation: fadeSlideUp 0.8s ease 0.4s both;"><div class="feature-icon">📈</div><div class="feature-title">Prophet Forecasting</div><div class="feature-desc">Advanced machine learning detects weekly seasonality to project highly accurate 30-day revenue models.</div></div>
<div class="feature-card" style="animation: fadeSlideUp 0.8s ease 0.5s both;"><div class="feature-icon">⚠️</div><div class="feature-title">Anomaly Detection</div><div class="feature-desc">Scikit-Learn's Isolation Forests monitor your data continuously to flag catastrophic drops or suspicious spikes.</div></div>
<div class="feature-card" style="animation: fadeSlideUp 0.8s ease 0.6s both;"><div class="feature-icon">🎯</div><div class="feature-title">Customer RFM Risk</div><div class="feature-desc">Automatically categorizes users by Recency, Frequency, and Monetary value to instantly identify churn risk.</div></div>
</div>
<p style="color: #64748b; font-size: 0.9rem; margin-top: 2rem;">
👈 <strong>Awaiting Data Input.</strong> Drop your dataset (CSV, Excel, JSON, or Parquet) into the secure zone on the left to initialize the engine.</p>
</div>
""", unsafe_allow_html=True)

    # ROUTE 2: DASHBOARD MODE (Either Demo Data or Uploaded Data)
    else:
        if st.session_state.use_demo:
            df = generate_demo_data()
            st.sidebar.markdown("---")
            st.sidebar.info("🧪 **Demo Mode Active**")
            if st.sidebar.button("Exit Demo Mode", use_container_width=True):
                st.session_state.use_demo = False
                st.rerun()
        else:
            df = load_data(uploaded_file)

    
        # ... your existing rendering code continues down here!
        
        if df is not None:
            st.sidebar.markdown("---")
            st.sidebar.title("⚙️ Column Mapping")
            st.sidebar.markdown("We attempted to auto-detect your columns. Please adjust if incorrect:")
            
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            all_cols = df.columns.tolist()
            
            def get_default(candidates, options):
                if not options: return 0
                for c in candidates:
                    for opt in options:
                        if c in str(opt).lower(): return options.index(opt)
                return 0

            sales_col = st.sidebar.selectbox("Sales/Value Column", numeric_cols if numeric_cols else ["None"], index=get_default(['sales', 'revenue', 'amount', 'total', 'price', 'profit'], numeric_cols))
            date_col = st.sidebar.selectbox("Date Column", all_cols + ["None"], index=get_default(['date', 'time', 'year'], all_cols))
            category_col = st.sidebar.selectbox("Category Column", all_cols + ["None"], index=get_default(['category', 'segment', 'type', 'dept'], all_cols))
            region_col = st.sidebar.selectbox("Region/Location Column", all_cols + ["None"], index=get_default(['region', 'state', 'city', 'country', 'loc'], all_cols))
            product_col = st.sidebar.selectbox("Product Column", all_cols + ["None"], index=get_default(['product', 'item', 'name', 'desc'], all_cols))
            customer_col = st.sidebar.selectbox("Customer ID Column", all_cols + ["None"], index=get_default(['customer', 'client', 'user', 'id'], all_cols))
            
            rename_dict = {}
            if sales_col and sales_col != "None": rename_dict[sales_col] = 'sales'
            if date_col and date_col != "None": rename_dict[date_col] = 'order_date'
            if category_col and category_col != "None": rename_dict[category_col] = 'category'
            if region_col and region_col != "None": rename_dict[region_col] = 'region'
            if product_col and product_col != "None": rename_dict[product_col] = 'product_name'
            if customer_col and customer_col != "None": rename_dict[customer_col] = 'customer_id'
            
            mapped_df = df.copy()
            mapped_df = mapped_df.rename(columns=rename_dict)
            
            mapped_df = mapped_df.loc[:, ~mapped_df.columns.duplicated()]
            
            if "order_date" in mapped_df.columns:
                mapped_df["order_date"] = pd.to_datetime(mapped_df["order_date"], errors='coerce')
                
            filtered_df = render_sidebar(mapped_df)
            
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "Dashboard", 
                "AI Insights", 
                "Forecast", 
                "Risk (RFM)", 
                "Chat AI", 
                "Data & Reports"
            ])
            
            with tab1:
                render_dashboard(filtered_df)
            with tab2:
                render_insights(filtered_df)
            with tab3:
                render_forecasting(filtered_df)
            with tab4:
                render_rfm_analysis(filtered_df)
            with tab5:
                render_chat_data(filtered_df)
            with tab6:
                render_data_view(filtered_df)

if __name__ == "__main__":
    main()