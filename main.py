import pandas as pd
import os
import streamlit as st
from datetime import datetime
import sys
from processing.extract.supabase_extractor import ExtractSupabaseProcessor
from processing.transform.dataframe_transformations import DataFrameTransformer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'processing')))

SUPABASE_URL = "https://dwltfqckbnzrlbvzhdha.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3bHRmcWNrYm56cmxidnpoZGhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzNjQ4NDEsImV4cCI6MjA1ODk0MDg0MX0.oxQUzlPCazMgXSQKNck-S03NXt-uvc36yjCpHvFOyy8"


supabase_extractor = ExtractSupabaseProcessor(
    base_url=SUPABASE_URL, api_key=SUPABASE_KEY
)

emp_hist_df = pd.DataFrame(supabase_extractor.extract("employment_history"))
users_df = pd.DataFrame(supabase_extractor.extract("users"))

user_emp_df = pd.merge(
    users_df,
    emp_hist_df,
    left_on="id",
    right_on="users_id",
    suffixes=("_users", "_emp"),
)

data_transformer = DataFrameTransformer()
user_emp_df = data_transformer.fill_null_dates_with_today(user_emp_df, "end_date")

# ---- Load Data ----
df = user_emp_df.sort_values(by="start_date", ascending=False)
df["start_date"] = pd.to_datetime(df["start_date"])
df["end_date"] = df["end_date"].replace("Present", datetime.now().strftime("%Y-%m-%d"))
df["end_date"] = pd.to_datetime(df["end_date"])

# ---- Page Config ----
st.set_page_config(layout="wide", page_title="Data Engineering CV")

# ---- Sidebar/Profile ----
st.sidebar.image("assets/images/profile_pic.jpg", width=150)
st.sidebar.title("Jasper Morgan")
st.sidebar.markdown("**Email:** jasper.morgan@hotmail.co.uk")
st.sidebar.markdown(
    "**GitHub:** [JasperMorgan93](https://github.com/JasperMorgan93/CvPortfolioApp)"
)
st.sidebar.markdown(
    "**LinkedIn:** [Jasper Morgan](https://www.linkedin.com/in/jasper-morgan-185841165/)"
)

# ---- Main Page ----
st.title("📄 Interactive Resume")
st.markdown("A visual and interactive version of my CV/portfolio, built in Python 💻")

# ---- Employment Timeline ----
import plotly.express as px

st.header("💼 Employment Timeline")
fig = px.timeline(
    df,
    x_start="start_date",
    x_end="end_date",
    y="company_name",
    color="role",
    hover_data=["role", "start_date", "end_date"],
)
fig.update_yaxes(autorange="reversed")
fig.update_layout(height=400)
fig.update_layout(yaxis_title="Employer")
st.plotly_chart(fig, use_container_width=True)


# ---- Job Descriptions ----
st.header("📋 Job Descriptions")
for idx, row in df.iterrows():
    st.subheader(f"{row['role']} - {row['company_name']}")
    st.caption(f"{row['start_date'].date()} → {row['end_date'].date()}")
    st.markdown(
        f"**Description:** {row.get('description', 'No description provided.')}"
    )
    if "skills" in row:
        st.markdown(f"**Skills Used:** {row['skills']}")

# ---- Skills Cloud or Tags ----
st.header("🛠️ Skills")
skills = df["key_skills"].dropna().str.split(", ").explode().value_counts()
st.bar_chart(skills)
