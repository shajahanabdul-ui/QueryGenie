"""
Generates a realistic synthetic HR analytics dataset and loads it into SQLite.
Run this once before starting the app: python setup_data.py
"""
import sqlite3
import numpy as np
import pandas as pd

np.random.seed(42)

N = 1470  # same scale as the well-known IBM HR Attrition dataset

departments = ["Sales", "Research & Development", "Human Resources"]
dept_weights = [0.31, 0.65, 0.04]

job_roles_by_dept = {
    "Sales": ["Sales Executive", "Sales Representative", "Manager"],
    "Research & Development": ["Research Scientist", "Laboratory Technician",
                                "Manufacturing Director", "Healthcare Representative", "Manager"],
    "Human Resources": ["Human Resources", "Manager"],
}

regions = ["North", "South", "East", "West", "Central"]

recruiters = ["Asha Rao", "Vikram Shah", "Priya Menon", "Daniel Cook",
              "Fatima Noor", "James Park", "Neha Kapoor", "Tom Reilly"]

rows = []
for i in range(1, N + 1):
    dept = np.random.choice(departments, p=dept_weights)
    role = np.random.choice(job_roles_by_dept[dept])
    region = np.random.choice(regions)
    age = int(np.clip(np.random.normal(37, 9), 20, 60))
    tenure_years = round(max(0, np.random.exponential(5)), 1)
    monthly_income = int(np.clip(np.random.normal(6500, 3500), 1800, 20000))
    satisfaction = np.random.randint(1, 5)  # 1-4
    performance_rating = np.random.choice([3, 4], p=[0.85, 0.15])
    distance_from_home = np.random.randint(1, 30)
    overtime = np.random.choice(["Yes", "No"], p=[0.28, 0.72])
    recruiter = np.random.choice(recruiters)

    # Attrition probability influenced by realistic factors
    attr_score = 0.10
    if satisfaction == 1: attr_score += 0.20
    if overtime == "Yes": attr_score += 0.15
    if tenure_years < 1: attr_score += 0.15
    if monthly_income < 3000: attr_score += 0.10
    if age < 25: attr_score += 0.10
    attrition = "Yes" if np.random.random() < min(attr_score, 0.85) else "No"

    rows.append({
        "employee_id": i,
        "age": age,
        "department": dept,
        "job_role": role,
        "region": region,
        "tenure_years": tenure_years,
        "monthly_income": monthly_income,
        "job_satisfaction": satisfaction,
        "performance_rating": performance_rating,
        "distance_from_home": distance_from_home,
        "overtime": overtime,
        "recruiter": recruiter,
        "attrition": attrition,
    })

df = pd.DataFrame(rows)

# A second small table so the assistant can show it's not just single-table --
# recruiter performance, referenced by "top-performing recruiters" style questions
recruiter_stats = (
    df.groupby("recruiter")
    .agg(hires=("employee_id", "count"),
         avg_tenure_of_hires=("tenure_years", "mean"))
    .reset_index()
)
recruiter_stats["avg_tenure_of_hires"] = recruiter_stats["avg_tenure_of_hires"].round(2)

conn = sqlite3.connect("hr_data.db")
df.to_sql("employees", conn, if_exists="replace", index=False)
recruiter_stats.to_sql("recruiter_performance", conn, if_exists="replace", index=False)
conn.close()

print(f"Done. hr_data.db created with {len(df)} employees.")
print("Tables: employees, recruiter_performance")
print("\nSample questions that will work well:")
print("  - Show attrition by department")
print("  - Which region has the highest attrition rate?")
print("  - What is the average monthly income by job role?")
print("  - Show top-performing recruiters by number of hires")
print("  - How does overtime affect attrition?")
