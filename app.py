"""
QueryGenie — Natural Language to Dashboard Query Assistant
Run with: streamlit run app.py
Requires: GEMINI_API_KEY environment variable set.
"""
import os
import re
import sqlite3
import json
import time
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai

st.set_page_config( page_title="QueryGenie",
                    page_icon="✨",
                    layout="wide",       
                    initial_sidebar_state="collapsed"
                   )

DB_PATH = "hr_data.db"
MODEL = "gemini-3.5-flash"

# ---------- Schema description given to the LLM as context ----------
SCHEMA_CONTEXT = """
You have access to a SQLite database with two tables:

Table: employees
- employee_id (INTEGER)
- age (INTEGER)
- department (TEXT) -- values: 'Sales', 'Research & Development', 'Human Resources'
- job_role (TEXT)
- region (TEXT) -- values: 'North', 'South', 'East', 'West', 'Central'
- tenure_years (REAL)
- monthly_income (INTEGER)
- job_satisfaction (INTEGER) -- 1 (low) to 4 (high)
- performance_rating (INTEGER) -- 3 or 4
- distance_from_home (INTEGER)
- overtime (TEXT) -- 'Yes' or 'No'
- recruiter (TEXT)
- attrition (TEXT) -- 'Yes' or 'No', whether the employee has left

Table: recruiter_performance
- recruiter (TEXT)
- hires (INTEGER)
- avg_tenure_of_hires (REAL)
"""

SYSTEM_PROMPT = f"""You are a SQL generation assistant for a business intelligence tool.
{SCHEMA_CONTEXT}

Given a business question in plain English, respond with ONLY a JSON object, no markdown, no explanation, in this exact shape:
{{"sql": "<a single valid SQLite SELECT statement>", "chart_type": "<bar|line|pie|table>", "x": "<column to use on x-axis or category, or null>", "y": "<column to use on y-axis or value, or null>"}}

Rules:
- Only ever generate SELECT statements. Never INSERT, UPDATE, DELETE, DROP, ALTER.
- Use column names exactly as given in the schema.
- For attrition rate questions, calculate it as (SUM(CASE WHEN attrition='Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)).
- Keep queries simple and single-statement.
- chart_type should be "bar" for comparisons across categories, "line" for anything over tenure/time, "pie" only for share-of-total questions, "table" if the result is a single number or doesn't chart well.
"""


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("GEMINI_API_KEY environment variable is not set.")
        st.stop()
    return genai.Client(api_key=api_key)


def is_safe_select(sql: str) -> bool:
    """Only allow single, read-only SELECT statements."""
    cleaned = sql.strip().rstrip(";")
    if ";" in cleaned:
        return False  # no stacked statements
    forbidden = r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|PRAGMA|REPLACE)\b"
    if re.search(forbidden, cleaned, re.IGNORECASE):
        return False
    return cleaned.strip().upper().startswith("SELECT")


def nl_to_sql(question: str):
    client = get_client()

    prompt = f"{SYSTEM_PROMPT}\n\nBusiness Question:\n{question}"

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    
    text = response.text.strip()

    text = re.sub(
        r"^```json|^```|```$",
        "",
        text,
        flags=re.MULTILINE
    ).strip()

    return json.loads(text)


def explain_result(question: str, df: pd.DataFrame):
    client = get_client()

    summary = {
    "rows_returned": len(df),
    "columns": list(df.columns),
    "sample_data": df.head(10).to_dict(orient="records")
}

    prompt = f"""
You are an experienced HR Analytics Consultant.

Your audience is HR Directors and Business Executives.

Based on the SQL results, identify trends rather than simply repeating the numbers.

Business Question:
{question}

SQL Result:
{json.dumps(summary, indent=2)}

Return ONLY a valid JSON object in the following format:

{{
    "insight":"",
    "recommendations":[
        "",
        "",
        ""
    ],
    "risks":[
        "",
        ""
    ],
    "followups":[
        "",
        "",
        ""
    ]
}}

Rules:

- insight should be 2-3 business sentences.
- recommendations should contain exactly 3 actionable recommendations.
- risks should contain exactly 2 risks.
- followups should contain exactly 3 natural language questions.
- Do not include markdown.
- Do not include explanations outside JSON.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    text = response.text.strip()

    text = re.sub(
        r"^```json|^```|```$",
         "",
        text,
        flags=re.MULTILINE
    ).strip()
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "insight": text,
            "recommendations": [],
            "risks": [],
            "followups": []
    }


def run_query(sql: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(sql, conn)
    finally:
        conn.close()
    return df


def render_chart(df,chart_type,x,y,title):
    if chart_type == "table" or df.shape[0] <= 1 or x not in df.columns:
        st.dataframe(df, width="stretch")
        return
    colors=[
        "#4F46E5",
        "#06B6D4",
        "#10B981",
        "#F59E0B",
        "#EF4444"
    ]

    if chart_type=="bar":
        fig=px.bar(df,x=x,y=y,color=x,text_auto=".2f",
                   color_discrete_sequence=colors)
    elif chart_type=="line":
        fig=px.line(df,x=x,y=y,markers=True)
    elif chart_type=="pie":
        fig=px.pie(df,names=x,values=y,hole=.45,
                   color_discrete_sequence=colors)
    else:
        st.dataframe(df, width="stretch")
        return

    fig.update_layout(
        title={"text":title,"x":0.5},
        template="plotly_dark",
        height=500,
        showlegend=False
    )
    st.plotly_chart(fig, width="stretch")
    



# ---------------------- UI ----------------------
st.title("✨ QueryGenie")

st.markdown("""
### 🤖 AI-Powered HR Analytics Assistant

Ask HR questions in plain English and instantly receive:

- 📝 SQL
- 📊 Interactive Visualization
- 💡 Executive Insights
- 🎯 Recommendations

---
""")

question=st.chat_input("Ask a question about HR data...")

if question:
    st.chat_message("user").write(question)

    start=time.time()

    with st.spinner("🤖 Understanding your question..."):
        try:
            parsed = nl_to_sql(question)
        except Exception as e:
            st.error(f"Couldn't generate SQL: {e}")
            st.stop()
        st.toast("✅ SQL Generated")

    sql=parsed["sql"]

    if not is_safe_select(sql):
        st.error("Unsafe SQL generated.")
        st.stop()

    with st.expander("📝 Generated SQL",expanded=True):
        st.code(sql,language="sql")

    with st.spinner("📊 Running query..."):
        try:
            df = run_query(sql)
            st.toast("📊 Data Retrieved")
        except Exception as e:
            st.error(f"Query failed: {e}")
            st.stop()

    response_time=round(time.time()-start,2)

    c1,c2,c3,c4=st.columns(4)
    c1.metric("Rows",len(df))
    c2.metric("Columns",len(df.columns))
    c3.metric("Response",f"{response_time}s")
    c4.metric("Chart",parsed.get("chart_type","table").upper())

    st.markdown("---")

    if not df.empty:
        render_chart(
            df,
            parsed.get("chart_type","table"),
            parsed.get("x"),
            parsed.get("y"),
            f"📊 {question}"
        )

        st.markdown("---")

        with st.spinner("💡 Generating Executive Insight..."):
            analysis = explain_result(question, df)

         # Executive Insight
        st.markdown("## 💡 Executive Insight")
        st.success(analysis["insight"])

         # Recommendations
        st.markdown("## 🎯 Recommendations")
        for rec in analysis.get("recommendations", []):
            st.write("✅", rec)
        
        # Risks
        st.markdown("## ⚠️ Potential Risks")
        for risk in analysis.get("risks",[]):
            st.write("⚠️", risk)

        #  Follow-up questions  
        st.markdown("## 🔍 Suggested Follow-up Questions")
        for q in analysis.get("followups",[]):
            st.info(q)

    else:
        st.warning("No data found.")
