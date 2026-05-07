# ⚡ AI-Powered Sales Analytics Dashboard

A modern, enterprise-grade business intelligence platform built with Python and Streamlit. This dashboard transforms raw sales data (CSV/Excel) into actionable insights using advanced machine learning, dynamic interactive visualizations, and Google's Generative AI (Gemini 2.5 Flash).

## 🚀 Features

* **🤖 Generative AI Chat**: Talk directly to your data. Integrated with Google Gemini 2.5 Flash to generate custom business recommendations based on real-time descriptive statistics of your dataset.
* **📈 Time-Series Forecasting**: Utilizes historical data trends and `numpy` linear polyfit models to generate reliable 30-day future sales projections.
* **⚠️ Customer Risk (RFM) Analysis**: Automatically scores customers based on Recency, Frequency, and Monetary value to identify high-value clients at risk of churning.
* **🎨 Dynamic Theming Engine**: Features a custom CSS architecture allowing users to instantly toggle between three premium dark-mode UI themes (Midnight Indigo, Cybernetic Teal, and Obsidian Slate).
* **📊 Interactive Visualizations**: Fully responsive Plotly charts with custom color sequences mapped to the active dashboard theme.
* **📄 Automated Reporting**: Download filtered datasets as CSVs or generate automated HTML Executive Summary reports for stakeholders.

---

## 📸 Screenshots

*(Replace these placeholder links with actual screenshots of your dashboard!)*

| Executive Dashboard | AI Data Chat | Risk Analysis (RFM) |
| :---: | :---: | :---: |
| <img src="https://via.placeholder.com/400x250.png?text=Dashboard+View" width="400"/> | <img src="https://via.placeholder.com/400x250.png?text=Chat+AI" width="400"/> | <img src="https://via.placeholder.com/400x250.png?text=RFM+Analysis" width="400"/> |

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

**3. Configure your API Key (Optional but recommended)**
To enable the "Chat AI" feature, you need a free Google Gemini API key.
* Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey).
* Create a `.streamlit` folder in the root directory.
* Create a file named `secrets.toml` inside that folder and add your key:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

**4. Run the Application**
```bash
streamlit run app.py
```

---

## 🛠️ Technologies Used

* **Frontend / Framework**: Streamlit, Custom CSS
* **Data Processing**: Pandas, NumPy
* **Data Visualization**: Plotly Express, Plotly Graph Objects
* **Artificial Intelligence**: Google Generative AI (`gemini-2.5-flash`)

---

## 🔮 Future Improvements

- [ ] Transition from in-memory Pandas processing to `DuckDB` for handling datasets > 1 million rows.
- [ ] Implement secure user authentication for public cloud deployment.
- [ ] Add PDF export capabilities for the Executive Reports.
- [ ] Expand the Forecasting module to include ARIMA / Prophet models for advanced seasonality detection.

---
*Designed for modern data analytics and professional portfolio demonstration.*
