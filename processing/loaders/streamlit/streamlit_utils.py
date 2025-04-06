import streamlit as st
import pandas as pd
import plotly.express as px
import time


class StreamlitProcessor:

    data: pd.DataFrame
    app_name: str

    def __init__(self, data, app_name):
        self.data = data
        self.app_name = app_name

    def run_streamlit_app(self):
        """Orchestrator to configure the whole streamlit app"""
        self.config_page()
        self.config_sidebar()
        self.config_main_page()
        self.config_employment_timeline()
        self.config_job_descriptions()
        self.configure_skills_chart()

    def prepare_data(self):
        """Data preperation for streamlit processing"""
        self.data = self.data.sort_values(by="start_date", ascending=False)

    def config_page(self):
        st.set_page_config(layout="wide", page_title="Data Engineering CV")

    def config_sidebar(self):
        # st.sidebar.image("assets/images/profile_pic.jpg", width=150)
        st.sidebar.title("Jasper Morgan")
        st.sidebar.markdown("**Email:** jasper.morgan@hotmail.co.uk")
        st.sidebar.markdown(
            "**GitHub:** [JasperMorgan93](https://github.com/JasperMorgan93/CvPortfolioApp)"
        )
        st.sidebar.markdown(
            "**LinkedIn:** [Jasper Morgan](https://www.linkedin.com/in/jasper-morgan-185841165/)"
        )

    def config_main_page(self):
        st.title("Data Engineering CV")
        self.type_markdown("""
            Hi, welcome to my CV App.
                           
            I've created this as a more enjoyable way to look through a CV and showcase some of my skills/knowledge.
                           
            The data are hosted a SQL database using supabase, called it via the supabase API and presented the data here on Streamlit. 
                           
            You can view the code I used to create this app in the GitHub link in the sidebar.
            """
        )

    def config_employment_timeline(self):
        st.header("💼 Employment Timeline")
        fig = px.timeline(
            self.data,
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

    def config_job_descriptions(self):
        st.header("📋 Job Descriptions")
        for idx, row in self.data.iterrows():
            st.subheader(f"{row['role']} - {row['company_name']}")
            st.caption(f"{row['start_date'].date()} → {row['end_date'].date()}")
            with st.expander("See Description"):
                st.markdown(f"{row.get('description', 'No description provided.')}")
            if "skills" in row:
                st.markdown(f"**Skills Used:** {row['skills']}")

    def configure_skills_chart(self):
        st.header("🛠️ Skills")
        skills = (
            self.data["key_skills"].dropna().str.split(", ").explode().value_counts()
        )
        st.bar_chart(skills)

    def type_markdown(self, text, delay=0.01):
        placeholder = st.empty()
        current_text = ""
        for char in text:
            current_text += char
            placeholder.markdown(current_text)
            time.sleep(delay)

