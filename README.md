# ✨ QueryGenie

> **AI-Powered HR Analytics Assistant**
>
> Transform natural language questions into SQL, interactive dashboards, and executive business insights using **Google Gemini**, **Streamlit**, **SQLite**, and **Plotly**.

---

## 🚀 Overview

QueryGenie is an AI-powered Business Intelligence application that enables HR professionals and business users to analyze workforce data without writing SQL.

Ask questions in plain English such as:

> **"Which region has the highest attrition rate?"**

QueryGenie automatically:

- 🤖 Converts natural language into SQL
- 🔒 Validates SQL for safety
- 🗄️ Executes queries on SQLite
- 📊 Generates interactive dashboards
- 💡 Produces executive insights
- 🎯 Suggests business recommendations
- ⚠️ Highlights potential risks
- 🔍 Recommends follow-up analytical questions

---

# ✨ Features

- Natural Language → SQL using Google Gemini
- SQL Safety Validation
- Interactive Plotly Charts
- KPI Dashboard
- Executive Insights
- AI-Powered Business Recommendations
- Risk Analysis
- Suggested Follow-up Questions
- Modern Streamlit UI

---

# 🏗️ Architecture

```text
                   User Question
                         │
                         ▼
                Google Gemini 3.5 Flash
                         │
                  SQL Generation
                         │
                 SQL Safety Check
                         │
                      SQLite
                         │
                  Query Execution
                         │
           ┌─────────────┴─────────────┐
           ▼                           ▼
   Interactive Charts          AI Business Analysis
                                         │
                     ┌───────────────────┼────────────────────┐
                     ▼                   ▼                    ▼
            Executive Insight   Recommendations      Business Risks
                                         │
                                         ▼
                             Follow-up Questions
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Streamlit | Web Application |
| Google Gemini 3.5 Flash | AI SQL Generation & Business Analysis |
| SQLite | Database |
| Plotly | Interactive Visualizations |
| Pandas | Data Processing |
| python-dotenv | Environment Variables |

---

# 📂 Project Structure

```text
QueryGenie/
│
├── app.py
├── hr_data.db
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
├── screenshots/
│    ├── home.png
│    ├── sql.png
│    ├── dashboard.png
│    └── insights.png
└── .env
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/<your-github-username>/QueryGenie.git
```

Go to the project folder

```bash
cd QueryGenie
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application

```bash
streamlit run app.py
```

---

# 💬 Sample Questions

- Show attrition by department
- Which region has the highest attrition rate?
- How does overtime affect attrition?
- Show average monthly income by job role
- Show top-performing recruiters by number of hires
- Compare average salary across regions
- Show average performance rating by department
- Which department has the highest employee satisfaction?

---

# 🔒 Security

Only read-only **SELECT** statements are executed.

The application blocks SQL operations such as:

- INSERT
- UPDATE
- DELETE
- DROP
- ALTER
- CREATE
- ATTACH
- PRAGMA
- REPLACE

---

# 📸 Screenshots

Add screenshots after deployment.

## 📸 Home Screen

```
screenshots/
    home.png
    sql.png
    dashboard.png
    insights.png
```

---

# 🚀 Future Enhancements

- Executive Dashboard
- Multi-database Support (Snowflake, PostgreSQL, BigQuery)
- Authentication & User Management
- Conversation History
- Export Reports (PDF/Excel)
- Voice-based Analytics
- Dashboard Sharing

---

# 👨‍💻 Author

**Shajahan Abdul**

Business Intelligence Partner | Data Analytics | AI Enthusiast

---

# ⭐ Acknowledgements

Built using:

- Google Gemini
- Streamlit
- Plotly
- SQLite
- Pandas

---

## ⭐ If you found this project interesting, please consider giving it a Star!
