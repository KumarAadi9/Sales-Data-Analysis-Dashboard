import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io
import json
import os
import hashlib

# ==========================================
# 1. THEME CONFIGURATIONS & STYLING
# ==========================================
THEMES = {
    "Midnight Indigo": {
        "bg": "#0F111A", "card_bg": "#161824", "border": "rgba(255, 255, 255, 0.05)",
        "primary": "#6366F1", "secondary": "#A855F7", "text_primary": "#F8FAFC", "text_secondary": "#94A3B8",
        "chart_colors": ['#6366F1', '#A855F7', '#EC4899', '#14B8A6', '#F59E0B']
    },
    "Cybernetic Teal": {
        "bg": "#0B0E14", "card_bg": "#11161F", "border": "#1E293B",
        "primary": "#10B981", "secondary": "#06B6D4", "text_primary": "#FFFFFF", "text_secondary": "#64748B",
        "chart_colors": ['#10B981', '#06B6D4', '#3B82F6', '#8B5CF6', '#F43F5E']
    },
    "Obsidian Slate": {
        "bg": "#121212", "card_bg": "#1E1E1E", "border": "#333333",
        "primary": "#FFFFFF", "secondary": "#3B82F6", "text_primary": "#E0E0E0", "text_secondary": "#888888",
        "chart_colors": ['#60A5FA', '#34D399', '#FBBF24', '#F87171', '#A78BFA']
    }
}

def apply_theme():
    """Injects custom CSS based on the currently selected theme."""
    t = THEMES[st.session_state.theme]
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Outfit', sans-serif;
    }}
    
    .stApp {{
        background-color: {t['bg']};
    }}
    
    [data-testid="stHeader"] {{background-color: transparent;}}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}

    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px !important;
    }}
    
    h1, h2, h3, h4, h5, h6, .markdown-text-container {{
        color: {t['text_primary']} !important;
    }}
    
    h1, h2, h3 {{
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }}

    p, li {{
        color: {t['text_secondary']};
    }}

    /* Beautiful Gradient KPI Cards */
    div[data-testid="metric-container"] {{
        background: {t['card_bg']};
        border-radius: 16px;
        padding: 1.8rem;
        border: 1px solid {t['border']};
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease-in-out;
    }}

    div[data-testid="metric-container"]:hover {{
        transform: translateY(-4px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
        border-color: {t['primary']};
    }}
    
    div[data-testid="metric-container"] label {{
        color: {t['text_secondary']} !important;
        font-weight: 500 !important;
        font-size: 1.05rem !important;
        margin-bottom: 0.5rem;
    }}
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {{
        color: {t['text_primary']} !important;
        font-weight: 700 !important;
        font-size: 2.2rem !important;
        background: -webkit-linear-gradient(45deg, {t['primary']}, {t['secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    /* Chart Containers */
    [data-testid="stPlotlyChart"] {{
        background-color: {t['card_bg']};
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        border: 1px solid {t['border']};
        overflow: hidden;
    }}

    .streamlit-expanderHeader {{
        background-color: {t['card_bg']};
        border-radius: 8px;
    }}
    
    hr {{
        margin: 2rem 0;
        border-color: {t['border']};
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {t['bg']};
        border-right: 1px solid {t['border']};
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
        background-color: transparent;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 3rem;
        background-color: transparent;
        color: {t['text_secondary']};
        font-weight: 500;
        font-size: 1.1rem;
    }}
    .stTabs [aria-selected="true"] {{
        color: {t['text_primary']} !important;
        border-bottom-color: {t['primary']} !important;
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        background-color: {t['primary']};
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
                template="plotly_dark"
            )
            fig_trend.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=40, b=20),
                xaxis_title="", yaxis_title="Sales ($)",
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
    with row1_col2:
        if "category" in df.columns and "sales" in df.columns:
            st.subheader("Sales by Category")
            sales_cat = df.groupby("category")["sales"].sum().reset_index()
            fig_cat = px.pie(
                sales_cat, names="category", values="sales", hole=0.5,
                color_discrete_sequence=THEMES[st.session_state.theme]['chart_colors'],
                template="plotly_dark"
            )
            fig_cat.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            fig_cat.update_traces(textposition='inside', textinfo='percent', hoverinfo='label+percent+value')
            st.plotly_chart(fig_cat, use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
            
    # --- CHARTS SECTION 2: Region & Products ---
    row2_col1, row2_col2 = st.columns(2, gap="large")
    
    with row2_col1:
        if "region" in df.columns and "sales" in df.columns:
            st.subheader("Regional Performance")
            sales_region = df.groupby("region")["sales"].sum().reset_index().sort_values("sales", ascending=True)
            fig_region = px.bar(
                sales_region, y="region", x="sales", orientation='h',
                color_discrete_sequence=[THEMES[st.session_state.theme]['primary']],
                template="plotly_dark"
            )
            fig_region.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=40, b=20), coloraxis_showscale=False,
                xaxis_title="Sales ($)", yaxis_title="",
                xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(showgrid=False)
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
                template="plotly_dark"
            )
            fig_top.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=40, b=20), coloraxis_showscale=False,
                xaxis_title="Sales ($)", yaxis_title="",
                xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(showgrid=False)
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
    st.dataframe(df, use_container_width=True)

# ==========================================
# 6. AI & BUSINESS INSIGHTS
# ==========================================
def render_insights(df):
    """Generates automated business insights based on the filtered data."""
    st.header("🤖 AI-Powered Business Insights")
    st.markdown("Discover actionable, data-driven recommendations tailored to your current performance.")
    
    if df.empty:
        st.warning("Not enough data to generate insights.")
        return

    st.markdown("---")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.subheader("📈 Performance & Trends")
        
        # 1. Top-Performing Regions
        if "region" in df.columns and "sales" in df.columns:
            region_sales = df.groupby("region")["sales"].sum().sort_values(ascending=False)
            if not region_sales.empty and region_sales.sum() > 0:
                top_region = region_sales.index[0]
                top_pct = (region_sales.iloc[0] / region_sales.sum()) * 100
                st.info(f"**Regional Outperformance**: **{top_region}** leads revenue generation, contributing **{top_pct:.1f}%** of total sales. Recommend allocating expansion capital to this high-yield market.")

        # 2. Declining Sales Trends
        if "order_date" in df.columns and "sales" in df.columns:
            trend_df = df.dropna(subset=['order_date']).copy()
            if not trend_df.empty:
                sales_by_month = trend_df.groupby(trend_df['order_date'].dt.to_period('M'))['sales'].sum()
                if len(sales_by_month) >= 3:
                    m1, m2, m3 = sales_by_month.iloc[-3], sales_by_month.iloc[-2], sales_by_month.iloc[-1]
                    if m3 < m2 and m2 < m1:
                        decline_pct = ((m1 - m3) / m1) * 100 if m1 > 0 else 0
                        st.warning(f"**Sales Contraction**: Revenue declined for two consecutive months (down **{decline_pct:.1f}%** from peak). Immediate review of pipeline velocity and demand generation required.")
                    elif m3 < m2:
                        decline_pct = ((m2 - m3) / m2) * 100 if m2 > 0 else 0
                        st.warning(f"**Short-Term Decline**: Recent month sales contracted by **{decline_pct:.1f}%**. Investigate potential seasonality or recent marketing inefficiencies.")
                    else:
                        growth_pct = ((m3 - m2) / m2) * 100 if m2 > 0 else 0
                        st.success(f"**Growth Trajectory**: Sales grew by **{growth_pct:.1f}%** in the most recent period. Current go-to-market strategy is effective.")

        # 3. Seasonal Patterns
        if "order_date" in df.columns and "sales" in df.columns:
            trend_df = df.dropna(subset=['order_date']).copy()
            if not trend_df.empty:
                trend_df['quarter'] = trend_df['order_date'].dt.quarter
                q_sales = trend_df.groupby('quarter')['sales'].mean()
                if len(q_sales) > 1:
                    best_q = q_sales.idxmax()
                    st.info(f"**Seasonality Detection**: Average revenue peaks in **Q{best_q}**. Align inventory procurement and marketing spend to capitalize on this recurring demand surge.")

    with col2:
        st.subheader("💡 Profitability & Behavior")
        
        # 4. Profitable Categories
        if "category" in df.columns and "profit" in df.columns and "sales" in df.columns:
            cat_profit = df.groupby("category")[["sales", "profit"]].sum()
            cat_profit = cat_profit[cat_profit["sales"] > 0]
            if not cat_profit.empty:
                cat_profit["margin"] = (cat_profit["profit"] / cat_profit["sales"]) * 100
                most_profitable = cat_profit.sort_values(by="margin", ascending=False).index[0]
                best_margin = cat_profit["margin"].max()
                st.success(f"**Category Profitability**: **{most_profitable}** is the most lucrative segment with a **{best_margin:.1f}%** profit margin. Prioritize this category in upcoming promotional cycles.")
                
        # 5. Loss-Making Products
        prod_col = "product_name" if "product_name" in df.columns else "product" if "product" in df.columns else None
        if prod_col and "profit" in df.columns:
            prod_profit = df.groupby(prod_col)["profit"].sum().sort_values(ascending=True)
            loss_prods = prod_profit[prod_profit < 0]
            if not loss_prods.empty:
                worst_prod = loss_prods.index[0]
                worst_prod_name = worst_prod if len(str(worst_prod)) < 35 else f"{str(worst_prod)[:32]}..."
                total_loss = abs(loss_prods.sum())
                st.error(f"**Profit Drain**: **{len(loss_prods)}** products operate at a net loss, costing **${total_loss:,.0f}**. The worst offender is '{worst_prod_name}'. Consider immediate discontinuation or price restructuring.")

        # 6. Customer Purchasing Behavior
        if "sales" in df.columns and "order_id" in df.columns:
            unique_orders = df["order_id"].nunique()
            if unique_orders > 0:
                aov = df["sales"].sum() / unique_orders
                items_per_order = len(df) / unique_orders
                st.info(f"**Purchasing Behavior**: Average Order Value (AOV) is **${aov:.2f}** with **{items_per_order:.1f}** items per transaction. Introduce volume-based discounts to increase basket size.")

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
        
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
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
    
    rfm = df.groupby(customer_col).agg({
        'order_date': lambda x: (current_date - x.max()).days, # Recency
        'order_id': 'nunique' if 'order_id' in df.columns else 'count', # Frequency
        'sales': 'sum' # Monetary
    }).reset_index()
    
    rfm.rename(columns={'order_date': 'Recency (Days)', 'order_id': 'Frequency', 'sales': 'Total Spend ($)'}, inplace=True)
    
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
        st.dataframe(at_risk.sort_values('Total Spend ($)', ascending=False).head(10), use_container_width=True)
        
    with col2:
        fig = px.scatter(rfm, x='Recency (Days)', y='Total Spend ($)', color='R', 
                         hover_name=customer_col, size='Frequency',
                         title="Recency vs Spend (Color: Recency Score)",
                         color_continuous_scale="RdYlGn")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
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
# 9.5. AUTHENTICATION SYSTEM
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

def render_login():
    st.markdown("<h1 style='text-align: center; margin-top: 5rem;'>🔐 AI Sales Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Please log in or sign up to access the enterprise portal.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                st.markdown("### Log In")
                email_or_phone = st.text_input("Email or Mobile Number")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", use_container_width=True)
                
                if submit:
                    if authenticate(email_or_phone, password):
                        st.session_state.logged_in = True
                        st.session_state.current_user = email_or_phone
                        st.rerun()
                    else:
                        st.error("Invalid email/phone or password.")
                        
        with tab2:
            with st.form("signup_form"):
                st.markdown("### Create an Account")
                new_email_or_phone = st.text_input("Email or Mobile Number")
                new_password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                signup_submit = st.form_submit_button("Sign Up", use_container_width=True)
                
                if signup_submit:
                    if new_password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters.")
                    elif not new_email_or_phone:
                        st.error("Please enter a valid email or mobile number.")
                    else:
                        if save_user(new_email_or_phone, new_password):
                            st.success("Account created successfully! Please switch to the Login tab.")
                        else:
                            st.error("An account with this email/phone already exists.")

# ==========================================
# 10. MAIN APPLICATION ROUTER
# ==========================================
def main():
    st.set_page_config(
        page_title="AI-Powered Sales Dashboard",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    if 'theme' not in st.session_state:
        st.session_state.theme = "Midnight Indigo"
        
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.current_user = None
        
    apply_theme()
    
    # ------------------------------------------
    # Authentication Check
    # ------------------------------------------
    if not st.session_state.logged_in:
        render_login()
        return
        
    # Sidebar Profile & Logout
    st.sidebar.markdown(f"👤 Logged in as: **{st.session_state.current_user}**")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
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
            # Render filters
            filtered_df = render_sidebar(df)
            
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