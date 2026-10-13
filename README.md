# ⚡ AI-Powered Sales Analytics Dashboard

A modern, enterprise-grade business intelligence platform built with Python and Streamlit. This dashboard transforms raw sales data (CSV, Excel, JSON, Parquet) into actionable insights using machine learning, interactive visualizations, and Google's Generative AI (Gemini 2.5 Flash).

<!-- TODO: add your live Streamlit Community Cloud link here, e.g. **Live demo:** https://your-app.streamlit.app -->

## 🚀 Features

* **🔐 Secure Authentication**: Sign-up and login backed by SQLite, with passwords hashed using `bcrypt`. Includes an email-based confirmation-code password reset and a persistent login via browser cookie. Each user's theme preference is saved to their account.
* **📊 Interactive Dashboard**: KPI cards (total sales, profit or average order value, total orders), monthly sales trend, sales by category, regional performance, and top 10 products, all as Plotly charts styled to the active theme.
* **📈 Time-Series Forecasting**: Uses Meta's **Prophet** to model historical daily sales and project the next 30 days, with a confidence interval. The trained model is cached so repeated views load instantly.
* **⚠️ Anomaly Detection**: A scikit-learn **Isolation Forest** flags irregular sales days and highlights them on the daily sales line.
* **🎯 Customer Risk (RFM) Analysis**: Scores customers on Recency, Frequency, and Monetary value (terciles, 1–3). High-value customers with low recency are flagged as churn risks, with a risk level (low, intermediate, critical), revenue at risk, and a suggested action plan.
* **🤖 Generative AI**: Google Gemini 2.5 Flash generates business insights from dataset summary statistics, and a chat assistant answers plain-English questions about your data.
* **📄 Automated Reporting**: Download the filtered dataset as CSV, an HTML executive summary, or a PDF executive report that embeds the dashboard charts.
* **🧩 Flexible Data Input**: Supports CSV, XLSX/XLS, JSON, and Parquet uploads, with a column-mapping panel that auto-detects sales, date, category, region, product, and customer columns. A one-click demo dataset is included for testing.
* **🎨 Dynamic Theming Engine**: Custom CSS architecture that lets users switch between multiple premium dark UI themes instantly.

---

## 📸 Screenshots

*(Replace these placeholder links with actual screenshots of your dashboard!)*

| Executive Dashboard | AI Data Chat | Risk Analysis (RFM) |
| :---: | :---: | :---: |
| <img src="https://via.placeholder.com/400x250.png?text=Dashboard+View" width="400"/> | <img src="https://via.placeholder.com/400x250.png?text=Chat+AI" width="400"/> | <img src="https://via.placeholder.com/400x250.png?text=RFM+Analysis" width="400"/> |

---

## 🗂️ Project Structure

| File | Purpose |
| :--- | :--- |
| `app.py` | Main Streamlit app: data loading, filters, dashboard, forecasting, RFM, AI features, and routing |
| `auth.py` | User sign-up, login (bcrypt), password reset, reset email, and theme persistence (SQLite) |
| `reports.py` | PDF executive report generation (FPDF + Plotly charts exported via Kaleido) |
| `styles.py` | Theme definitions and custom CSS |
| `model_training.ipynb` | Notebook used for Prophet model training and experimentation |
| `packages.txt` | System packages for deployment (Chromium, required by Kaleido for chart export) |
| `data/` | Sample data |

---

## 💻 Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/KumarAadi9/Sales-Data-Analysis-Dashboard.git
cd Sales-Data-Analysis-Dashboard
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure secrets**
To enable the Gemini features, you need a free Google Gemini API key.
* Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey).
* Create a `.streamlit` folder in the root directory (if it does not exist).
* Create a file named `secrets.toml` inside that folder and add your key:
```toml
GEMINI_API_KEY = "your-api-key-here"
```
The key can also be provided as the `GEMINI_API_KEY` environment variable, or entered in the **Chat AI** tab for the current session.

To enable password-reset emails (sent through Gmail SMTP), also add a sender account to the same `secrets.toml`. Use a Gmail [App Password](https://support.google.com/accounts/answer/185833), not your normal password:
```toml
EMAIL_SENDER = "your-sender@gmail.com"
EMAIL_PASS = "your-gmail-app-password"
```

> Never commit `secrets.toml` or the SQLite database to GitHub.

**4. Run the Application**
```bash
streamlit run app.py
```

No data handy? Click **Load Enterprise Demo Data** in the sidebar to try every feature.

---

## 📥 Input Data

For best results, your file should contain these columns (names are auto-detected and can be remapped in the sidebar):

| Column | Type | Used for |
| :--- | :--- | :--- |
| `order_date` | Date | Trends, forecasting, anomaly detection, RFM |
| `sales` | Number | All KPIs and models |
| `profit` | Number | Profit KPI (optional) |
| `region` | Text | Regional performance and filters |
| `category` | Text | Category breakdown and filters |
| `customer_id` | Text/Number | RFM and churn analysis |

---

## 🛠️ Technologies Used

* **Frontend / Framework**: Streamlit, Custom CSS
* **Data Processing**: Pandas, NumPy
* **Data Visualization**: Plotly Express, Plotly Graph Objects
* **Machine Learning**: Prophet (forecasting), scikit-learn (Isolation Forest anomaly detection)
* **Artificial Intelligence**: Google Generative AI (`gemini-2.5-flash`)
* **Authentication & Storage**: SQLite, bcrypt, streamlit-cookies-controller
* **Reporting**: FPDF, Kaleido (Plotly static image export)

---

## 🔮 Future Improvements

- [ ] Transition from in-memory Pandas processing to `DuckDB` for handling datasets > 1 million rows.
- [ ] Migrate user storage from SQLite to PostgreSQL for multi-user production use.
- [ ] Add expiry and attempt limits to password-reset codes, and sign the login cookie.
- [ ] Add in-app forecast validation (hold-out error metrics) and holiday regressors.
- [ ] Expand the Forecasting module with ARIMA as a baseline comparison.

---
*Designed for modern data analytics and professional portfolio demonstration.*
