import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io
import json
import os
import hashlib
import random
import jinja2
from streamlit_cookies_controller import CookieController

# ==========================================
# 1. THEME CONFIGURATIONS & STYLING
# ==========================================

THEMES = {
    "Neon Cyberpunk": {
        "bg": "#09090b", "card_bg": "#18181b", "sidebar_bg": "#09090b", "border": "#27272a",
        "primary": "#f472b6", "secondary": "#22d3ee", "text_primary": "#f8fafc", "text_secondary": "#a1a1aa",
        "chart_colors": ['#f472b6', '#22d3ee', '#a855f7', '#fb923c', '#4ade80'], # Hot pink, cyan, purple, neon orange, lime
        "plotly_template": "plotly_dark"
    },
    "Matcha Cloud": {
        "bg": "#fafaf9", "card_bg": "#ffffff", "sidebar_bg": "#f5f5f4", "border": "#e7e5e4",
        "primary": "#a3e635", "secondary": "#fbcfe8", "text_primary": "#1c1917", "text_secondary": "#78716c",
        "chart_colors": ['#a3e635', '#fbcfe8', '#bfdbfe', '#fde047', '#c4b5fd'], # Matcha, soft pink, baby blue, pastel yellow, lavender
        "plotly_template": "plotly_white"
    },
    "Y2K Vaporwave": {
        "bg": "#1e1b4b", "card_bg": "#312e81", "sidebar_bg": "#2e1065", "border": "#4c1d95",
        "primary": "#ff00ff", "secondary": "#00ffff", "text_primary": "#ffffff", "text_secondary": "#c7d2fe",
        "chart_colors": ['#ff00ff', '#00ffff', '#fbbf24', '#f43f5e', '#8b5cf6'], # Magenta, Cyan, Gold, Rose, Violet
        "plotly_template": "plotly_dark"
    },
    "Dark Espresso": {
        "bg": "#1c1917", "card_bg": "#292524", "sidebar_bg": "#1c1917", "border": "#44403c",
        "primary": "#d97706", "secondary": "#fcd34d", "text_primary": "#fafaf9", "text_secondary": "#a8a29e",
        "chart_colors": ['#d97706', '#fcd34d', '#78350f', '#fb923c', '#b45309'], # Amber, cream, deep roast, orange
        "plotly_template": "plotly_dark"
    },
    "Enterprise Light": {
        "bg": "#F8FAFC", "card_bg": "#FFFFFF", "sidebar_bg": "#FFFFFF", "border": "#E2E8F0",
        "primary": "#2563EB", "secondary": "#3B82F6", "text_primary": "#0F172A", "text_secondary": "#64748B",
        "chart_colors": ['#2563EB', '#10B981', '#F59E0B', '#6366F1', '#8B5CF6'],
        "plotly_template": "plotly_white"
    },
    "Enterprise Dark": {
        "bg": "#0B0F19", "card_bg": "#111827", "sidebar_bg": "#111827", "border": "#1F2937",
        "primary": "#3B82F6", "secondary": "#60A5FA", "text_primary": "#F9FAFB", "text_secondary": "#9CA3AF",
        "chart_colors": ['#3B82F6', '#10B981', '#FBBF24', '#818CF8', '#A78BFA'],
        "plotly_template": "plotly_dark"
    }
}


def apply_theme():
    """Injects custom CSS based on the currently selected theme for an Enterprise SaaS look."""
    t = THEMES[st.session_state.theme]
    
    st.markdown(f"""
    <style>
    /* Premium SaaS Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], span, label, p, div {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        letter-spacing: -0.01em;
    }}
    
    .stApp {{ background-color: {t['bg']}; }}
    
    /* Clean Sidebar */
    [data-testid="stSidebar"] > div:first-child {{
        background-color: {t['sidebar_bg']} !important;
        border-right: 1px solid {t['border']} !important;
    }}
    
    /* Input Widgets & Dropdowns */
    div[data-baseweb="select"] > div, input {{
        background-color: {t['card_bg']} !important;
        color: {t['text_primary']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: 6px !important;
        font-size: 0.9rem !important;
    }}
    
    div[data-baseweb="popover"] > div, div[data-baseweb="popover"] ul, ul[role="listbox"] {{
        background-color: {t['card_bg']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: 6px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    }}
    li[role="option"] {{ color: {t['text_primary']} !important; font-size: 0.9rem !important; }}
    li[role="option"]:hover, li[aria-selected="true"] {{ background-color: {t['bg']} !important; color: {t['primary']} !important; }}
    
    /* Global Text Hierarchy */
    h1, h2, h3, h4, h5, h6 {{ color: {t['text_primary']} !important; font-weight: 600 !important; letter-spacing: -0.02em; }}
    p, li, .st-emotion-cache-1wivap2 {{ color: {t['text_secondary']} !important; line-height: 1.6; }}
    
    [data-testid="stHeader"] {{ background-color: transparent; }}
    #MainMenu, footer, .stDeployButton {{ display: none; }}

    .block-container {{ padding-top: 2rem !important; padding-bottom: 3rem !important; max-width: 1400px !important; }}

    /* SaaS Enterprise KPI Cards */
    div[data-testid="metric-container"] {{
        background: {t['card_bg']};
        border-radius: 8px; /* Professional sharp corners */
        padding: 1.5rem;
        border: 1px solid {t['border']};
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        transition: box-shadow 0.2s ease-in-out;
    }}

    div[data-testid="metric-container"]:hover {{
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }}
    
    /* KPI Typography Hierarchy */
    div[data-testid="stMetricLabel"] {{
        color: {t['text_secondary']} !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }}
    
    div[data-testid="stMetricValue"] {{
        color: {t['text_primary']} !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        letter-spacing: -0.02em;
    }}

    /* Chart Containers */
    [data-testid="stPlotlyChart"] {{
        background-color: {t['card_bg']};
        border-radius: 8px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        border: 1px solid {t['border']};
        padding: 1rem;
        box-sizing: border-box; /* Forces padding inward to prevent clipping */
    }}

    /* Minimal Tabs */
    .stTabs [data-baseweb="tab-list"] {{ gap: 2rem; background-color: transparent; border-bottom: 1px solid {t['border']}; }}
    .stTabs [data-baseweb="tab"] {{ height: 3rem; background-color: transparent; color: {t['text_secondary']} !important; font-weight: 500; font-size: 1rem; padding-bottom: 0; }}
    .stTabs [aria-selected="true"] {{ color: {t['text_primary']} !important; border-bottom: 2px solid {t['primary']} !important; }}
    .stTabs [data-baseweb="tab-highlight"] {{ display: none; }} /* Hide default heavy highlight */

    /* Professional Buttons */
    div.stButton > button, div.stDownloadButton > button, div.stFormSubmitButton > button {{
        background-color: {t['card_bg']} !important;
        color: {t['text_primary']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.15s ease-in-out;
    }}
    div.stButton > button:hover, div.stDownloadButton > button:hover, div.stFormSubmitButton > button:hover {{
        border-color: {t['primary']} !important;
        color: {t['primary']} !important;
        background-color: {t['bg']} !important;
    }}

    /* File Uploader Box */
    [data-testid="stFileUploadDropzone"] {{
        background-color: {t['card_bg']} !important;
        border: 1px dashed {t['border']} !important;
        border-radius: 8px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. DATA LOADING & PROCESSING
# ==========================================
@st.cache_data
def load_data(uploaded_file):
    """Loads CSV or Excel data and normalizes column names."""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding="latin1")
        else:
            df = pd.read_excel(uploaded_file)
            
        # Standardize column names (lowercase, replace spaces with underscores)
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        
        # Parse dates if order_date exists
        if "order_date" in df.columns:
            df["order_date"] = pd.to_datetime(df["order_date"], errors='coerce')
            
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# ==========================================
# 3. SIDEBAR CONTROLS & FILTERS
# ==========================================
def render_sidebar(df):
    """Renders the sidebar global data filters."""
    st.sidebar.title("🎨 Theme Settings")
    selected_theme = st.sidebar.selectbox("Select Theme", options=list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.theme))
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.title("🔍 Global Filters")
    st.sidebar.markdown("Filter your data across all tabs.")
    
    filtered_df = df.copy()
    
    # 3a. Date Range Filter
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
    
    # 3b. Region Filter
    if "region" in filtered_df.columns:
        regions = st.sidebar.multiselect("Select Region", options=sorted(df["region"].dropna().unique()))
        if regions:
            filtered_df = filtered_df[filtered_df["region"].isin(regions)]
            
    # 3c. Category Filter
    if "category" in filtered_df.columns:
        categories = st.sidebar.multiselect("Select Category", options=sorted(df["category"].dropna().unique()))
        if categories:
            filtered_df = filtered_df[filtered_df["category"].isin(categories)]
            
    return filtered_df

# ==========================================
# 4. DASHBOARD VIEW (KPIs & Charts)
# ==========================================
def render_dashboard(df):
    """Renders the main executive dashboard with metrics and visual charts."""
    st.header("Executive Sales Dashboard")
    t = THEMES[st.session_state.theme]
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    # --- KPI SECTION ---
    st.markdown("### Key Performance Indicators")
    total_sales = df["sales"].sum() if "sales" in df.columns else 0
    total_profit = df["profit"].sum() if "profit" in df.columns else 0
    total_orders = df["order_id"].nunique() if "order_id" in df.columns else len(df)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Total Orders", f"{total_orders:,}")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # --- CHARTS SECTION 1: Trend & Category ---
    row1_col1, row1_col2 = st.columns((2, 1), gap="large") # Trend gets more space
    
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
            
    # --- CHARTS SECTION 2: Region & Products ---
    row2_col1, row2_col2 = st.columns(2, gap="large")
    
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
        # Check for product_name or just product
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
            # Truncate long product names for better display
            fig_top.update_yaxes(ticktext=[f"{str(name)[:30]}..." if len(str(name)) > 30 else name for name in top_products[prod_col]], 
                                 tickvals=top_products[prod_col])
            st.plotly_chart(fig_top, use_container_width=True)

# ==========================================
# 5. DATA VIEW (Raw Data Table)
# ==========================================
def render_data_view(df):
    """Renders the raw interactive dataset view and download capabilities."""
    st.header("Dataset Details & Reports")
    st.write(f"Showing **{len(df):,}** rows based on current filters.")
    
    col1, col2 = st.columns(2)
    with col1:
        # CSV Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Report (CSV)",
            data=csv,
            file_name='sales_report.csv',
            mime='text/csv',
            use_container_width=True
        )
    with col2:
        # HTML Executive Report Download
        total_sales = df['sales'].sum() if 'sales' in df.columns else 0
        orders = df['order_id'].nunique() if 'order_id' in df.columns else len(df)
        html_content = f"""
        <html>
        <head><title>Executive Sales Report</title></head>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Executive Sales Summary Report</h2>
            <p>Generated automatically by the AI Sales Dashboard.</p>
            <hr>
            <h3>Key Metrics</h3>
            <ul>
                <li><b>Total Sales:</b> ${total_sales:,.2f}</li>
                <li><b>Total Orders:</b> {orders:,}</li>
                <li><b>Dataset Rows Analyzed:</b> {len(df):,}</li>
            </ul>
            <p><i>More detailed AI insights can be viewed live on the dashboard platform.</i></p>
        </body>
        </html>
        """
        st.download_button(
            label="📄 Download Executive Report (HTML)",
            data=html_content,
            file_name='executive_summary.html',
            mime='text/html',
            use_container_width=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    t = THEMES[st.session_state.theme]
    # Force the dataframe cells to match the current theme
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
    """Generates dynamic business insights using the Gemini LLM API."""
    st.header("🧠 Generative AI Business Insights")
    st.markdown("Actionable, data-driven recommendations analyzed in real-time by Google Gemini.")
    
    if df.empty:
        st.warning("Not enough data to generate insights.")
        return

    st.markdown("---")
    
    # 1. API Key Check (Reuses the key from your Chat Data tab)
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

    # 2. The AI Generation Trigger
    if st.button("✨ Generate Custom AI Insights", use_container_width=True):
        with st.spinner("Analyzing dataset patterns... this takes a few seconds."):
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                
                # Using Gemini 1.5 Flash for fast, cost-effective text generation
                model = genai.GenerativeModel('gemini-2.5-flash') 
                
                # 3. Create the Data Fingerprint
                # include='all' ensures we get stats on categorical data too (like top region, top product)
                summary_stats = df.describe(include='all').to_string()
                
                # 4. The Expert Prompt
                prompt = f"""
                You are an expert Chief Revenue Officer and Data Scientist analyzing a company's sales dataset.
                Here is the statistical summary of the dataset:
                
                {summary_stats}
                
                Based STRICTLY on these numbers, provide 4 highly actionable, distinct business insights. 
                Format your response with clean Markdown. Use emojis, headings, bullet points, and highlight key numbers in bold. 
                Do not use generic advice; tie everything to the specific data provided above.
                Categorize them clearly into two sections: 'Performance & Trends' and 'Portfolio & Behavior'.
                """
                
                response = model.generate_content(prompt)
                
                st.success("Analysis Complete!")
                
                # 5. Render the AI's Markdown Response
                st.markdown(
                    f"""
                    <div style="background-color: {THEMES[st.session_state.theme]['card_bg']}; 
                                padding: 2rem; 
                                border-radius: 12px; 
                                border: 1px solid {THEMES[st.session_state.theme]['border']};">
                        {response.text}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
            except Exception as e:
                st.error(f"Failed to generate insights. Make sure your API key is valid. Error details: {e}")

# ==========================================
# 7. FORECASTING & MACHINE LEARNING
# ==========================================
def render_forecasting(df):
    st.header("📈 Sales Forecasting (30-Day Projection)")
    st.markdown("Utilizes historical linear trends to project future performance.")
    
    if "order_date" not in df.columns or "sales" not in df.columns:
        st.warning("Forecasting requires 'order_date' and 'sales' columns.")
        return
        
    # Aggregate daily sales
    daily_sales = df.groupby(df['order_date'].dt.date)['sales'].sum().reset_index()
    daily_sales['order_date'] = pd.to_datetime(daily_sales['order_date'])
    daily_sales = daily_sales.sort_values('order_date')
    
    if len(daily_sales) < 30:
        st.warning("Not enough historical data for a reliable forecast (minimum 30 days required).")
        return
        
    # Moving Averages
    daily_sales['30-Day MA'] = daily_sales['sales'].rolling(window=30).mean()
    
    # Basic linear projection
    x = np.arange(len(daily_sales))
    y = daily_sales['sales'].fillna(0).values
    
    if len(x) > 1:
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        
        future_x = np.arange(len(daily_sales), len(daily_sales) + 30)
        future_y = p(future_x)
        
        last_date = daily_sales['order_date'].max()
        future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, 31)]
        future_df = pd.DataFrame({'order_date': future_dates, 'Forecasted Sales': future_y})
        
        import plotly.graph_objects as go
        fig = go.Figure()
        
        t = THEMES[st.session_state.theme]
        fig.add_trace(go.Scatter(x=daily_sales['order_date'], y=daily_sales['sales'], name='Actual Sales', line=dict(color=t['primary'], width=1), opacity=0.4))
        fig.add_trace(go.Scatter(x=daily_sales['order_date'], y=daily_sales['30-Day MA'], name='30-Day Trend', line=dict(color=t['secondary'], width=3)))
        fig.add_trace(go.Scatter(x=future_df['order_date'], y=future_df['Forecasted Sales'], name='30-Day Forecast (Linear)', line=dict(color=t['text_primary'], width=3, dash='dot')))
        
        t = THEMES[st.session_state.theme] # Get the current theme
        fig.update_layout(
            height=450, # ⬇️ FORCE the chart to be taller so nothing gets compressed
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            
            # ⬇️ Hard-coded bottom margin (b=80) to guarantee the dates stay inside the card
            margin=dict(l=20, r=50, t=60, b=80), 
            font=dict(color=t['text_secondary']), 
            
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=1.05, # Pushed slightly higher to clear the top of the graph
                xanchor="center", 
                x=0.5
            ),
            
            xaxis=dict(
                # Removed automargin to stop it from fighting Streamlit
                showgrid=False, 
                showline=True, linecolor=t['border'], linewidth=1,
                color=t['text_secondary'], tickfont=dict(color=t['text_secondary'])
            ),
            yaxis=dict(
                showgrid=True, gridcolor=t['border'], 
                showline=True, linecolor=t['border'], linewidth=1,
                color=t['text_secondary'], tickfont=dict(color=t['text_secondary'])
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info(f"**Projection Insight**: Based on historical linear trends, sales are projected to trend towards **${future_y[-1]:,.2f}** per day by the end of the next 30-day period.")

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
    
    # Identify At-Risk High-Value Customers (R=1, F=3/2, M=3/2)
    at_risk = rfm[(rfm['R'] == 1) & (rfm['M'] >= 2)]
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.error(f"**Action Required**: You have **{len(at_risk)}** high-value customers who haven't purchased recently. Immediate retention campaign recommended.")
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
        
        # Aggressively force all fonts, axes, and colorbars to match the theme
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20),
            font=dict(color=t['text_secondary']), # Forces the title text color
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
        st.markdown("""
        To enable real AI responses, please provide a free Google Gemini API Key:
        1. Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Enter it below to activate the assistant for this session:
        """)
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
                # Create a concise context from the dataframe to avoid token limits
                context = f"""
                Here is a summary of the sales dataset:
                Columns: {', '.join(df.columns)}
                Number of rows: {len(df)}
                
                Summary statistics:
                {df.describe().to_string()}
                
                Top 3 rows of data:
                {df.head(3).to_string()}
                
                Based on this specific data, answer the user's question. Be concise, professional, and reference specific numbers from the dataset if applicable.
                """
                
                response = model.generate_content(f"{context}\n\nUser Question: {user_query}")
                
                st.success("🤖 AI Response:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error generating response: {e}. (Make sure your API key is valid).")

# ==========================================
# ==========================================
# 9.5. ADVANCED AUTHENTICATION SYSTEM
# ==========================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

def save_user(email_or_phone, password):
    users = load_users()
    if email_or_phone in users:
        return False # User already exists
    users[email_or_phone] = hash_password(password)
    with open('users.json', 'w') as f:
        json.dump(users, f)
    return True

def authenticate(email_or_phone, password):
    users = load_users()
    if email_or_phone in users and users[email_or_phone] == hash_password(password):
        return True
    return False

def reset_password(email_or_phone, new_password):
    users = load_users()
    if email_or_phone in users:
        users[email_or_phone] = hash_password(new_password)
        with open('users.json', 'w') as f:
            json.dump(users, f)
        return True
    return False

def generate_otp():
    """Generates a 6-digit OTP."""
    return str(random.randint(100000, 999999))

def render_login(controller):
    st.markdown("<h1 style='text-align: center; margin-top: 5rem;'>🔐 AI Sales Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Secure enterprise portal access.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        tab1, tab2, tab3, tab4 = st.tabs(["🔑 Login", "📝 Sign Up", "🔄 Reset Password", "📱 OTP Login"])
        
        # --- TAB 1: STANDARD LOGIN ---
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
                        # SET COOKIE HERE
                        controller.set('logged_in_user', email_or_phone, max_age=86400)
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                        
        # --- TAB 2: SIGN UP ---
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

        # --- TAB 3: FORGOT PASSWORD ---
        with tab3:
            st.markdown("### Reset Password")
            reset_user = st.text_input("Enter your registered Email/Phone")
            new_reset_pass = st.text_input("New Password", type="password")
            
            if st.button("Update Password", use_container_width=True):
                if not reset_user or not new_reset_pass:
                    st.error("Please fill in all fields.")
                elif reset_password(reset_user, new_reset_pass):
                    st.success("Password updated! You can now log in.")
                else:
                    st.error("Account not found.")

        # --- TAB 4: OTP LOGIN ---
        with tab4:
            st.markdown("### Login via OTP")
            otp_user = st.text_input("Registered Email/Phone", key="otp_user")
            
            # Use session state to track if an OTP was sent
            if 'generated_otp' not in st.session_state:
                st.session_state.generated_otp = None
                
            if st.button("Send OTP", use_container_width=True):
                users = load_users()
                if otp_user in users:
                    # Generate and store OTP in session
                    st.session_state.generated_otp = generate_otp()
                    st.session_state.otp_target_user = otp_user
                    st.info(f"*(Simulation)* An OTP has been sent! Your code is: **{st.session_state.generated_otp}**")
                else:
                    st.error("Account not found.")
            
            # Only show verification box if OTP was generated
            if st.session_state.generated_otp:
                entered_otp = st.text_input("Enter 6-digit OTP")
                if st.button("Verify & Login", use_container_width=True):
                    if entered_otp == st.session_state.generated_otp and otp_user == st.session_state.otp_target_user:
                        st.session_state.logged_in = True
                        st.session_state.current_user = otp_user
                        st.session_state.generated_otp = None 
                        # SET COOKIE HERE
                        controller.set('logged_in_user', otp_user, max_age=86400)
                        st.rerun()
                    else:
                        st.error("Invalid or expired OTP.")

# ==========================================
# 10. MAIN APPLICATION ROUTER
# ==========================================
import time # ⬅️ Make sure this is imported!

def main():
    st.set_page_config(
        page_title="AI-Powered Sales Dashboard",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 1. Initialize Controller
    controller = CookieController()
    
    # ⏳ THE FIX: Force Python to wait 0.3 seconds so the browser can send the cookie!
    time.sleep(0.3) 
    
    if 'theme' not in st.session_state or st.session_state.theme not in THEMES:
        st.session_state.theme = "Neon Cyberpunk"
        
    # 2. Check for Cookie on Startup
    saved_user = controller.get('logged_in_user')
    if saved_user:
        st.session_state.logged_in = True
        st.session_state.current_user = saved_user
        
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.current_user = None
        
    apply_theme()
    
    # ------------------------------------------
    # Authentication Check
    # ------------------------------------------
    if not st.session_state.logged_in:
        render_login(controller)  # Pass the controller to the login function
        return
        
    # Sidebar Profile & Logout
    st.sidebar.markdown(f"👤 Logged in as: **{st.session_state.current_user}**")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        # 3. Destroy Cookie on Logout
        controller.remove('logged_in_user')
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
    st.sidebar.markdown("---")
    
    st.sidebar.title("📂 Data Upload")
    uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])
    
    if uploaded_file is None:
        st.title("Welcome to the AI Analytics Dashboard ✨")
        st.info("👈 Please upload your Sales Data (CSV or Excel) from the sidebar to begin.")
        
        st.markdown("""
        ### Features of this Dashboard:
        * **CSV and Excel Support**: Seamlessly process standard spreadsheet formats.
        * **Interactive Global Filters**: Filter by Date, Region, and Category from the sidebar.
        * **Modern UI & Responsive Design**: Adapts flawlessly to Light and Dark modes.
        * **Executive KPI Cards**: Track Sales, Profit, and Orders at a glance.
        * **Advanced Visualizations**: Top products, regional analysis, and monthly trends using Plotly.
        * **AI-Generated Insights**: Automated business recommendations to drive decision making.
        """)
    else:
        # Load and parse data
        df = load_data(uploaded_file)
        
        if df is not None:
            # ------------------------------------------
            # DYNAMIC COLUMN MAPPING
            # ------------------------------------------
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

            # Add "None" fallback
            sales_col = st.sidebar.selectbox("💰 Sales/Value Column", numeric_cols if numeric_cols else ["None"], index=get_default(['sales', 'revenue', 'amount', 'total', 'price', 'profit'], numeric_cols))
            date_col = st.sidebar.selectbox("📅 Date Column", all_cols + ["None"], index=get_default(['date', 'time', 'year'], all_cols))
            category_col = st.sidebar.selectbox("📦 Category Column", all_cols + ["None"], index=get_default(['category', 'segment', 'type', 'dept'], all_cols))
            region_col = st.sidebar.selectbox("🌍 Region/Location Column", all_cols + ["None"], index=get_default(['region', 'state', 'city', 'country', 'loc'], all_cols))
            product_col = st.sidebar.selectbox("🛒 Product Column", all_cols + ["None"], index=get_default(['product', 'item', 'name', 'desc'], all_cols))
            customer_col = st.sidebar.selectbox("👤 Customer ID Column", all_cols + ["None"], index=get_default(['customer', 'client', 'user', 'id'], all_cols))
            
            rename_dict = {}
            if sales_col and sales_col != "None": rename_dict[sales_col] = 'sales'
            if date_col and date_col != "None": rename_dict[date_col] = 'order_date'
            if category_col and category_col != "None": rename_dict[category_col] = 'category'
            if region_col and region_col != "None": rename_dict[region_col] = 'region'
            if product_col and product_col != "None": rename_dict[product_col] = 'product_name'
            if customer_col and customer_col != "None": rename_dict[customer_col] = 'customer_id'
            
            mapped_df = df.copy()
            mapped_df = mapped_df.rename(columns=rename_dict)
            
            # 🛠️ FIX: Drop duplicate columns that might occur from dynamic renaming
            mapped_df = mapped_df.loc[:, ~mapped_df.columns.duplicated()]
            
            if "order_date" in mapped_df.columns:
                mapped_df["order_date"] = pd.to_datetime(mapped_df["order_date"], errors='coerce')
                
            # Render filters
            filtered_df = render_sidebar(mapped_df)
            
            # Tabs for analytics
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "📊 Dashboard", 
                "🤖 AI Insights", 
                "📈 Forecast", 
                "⚠️ Risk (RFM)", 
                "💬 Chat AI", 
                "📥 Data & Reports"
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