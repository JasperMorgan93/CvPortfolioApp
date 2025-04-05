import streamlit as st
import pandas as pd
import plotly.express as px


class StreamlitProcessor:

    data : pd.DataFrame
    app_name : str

    def __init__(self, data, app_name):
        self.data = data
        self.app_name = app_name

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
        st.markdown("""
                    A visual and interactive version of my CV/portfolio. 
                    The data are loaded from SQL via the supabase API, 
                    processed in Python and presented via Streamlit
                    """)
        
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
            st.markdown(
                f"**Description:** {row.get('description', 'No description provided.')}"
            )
            if "skills" in row:
                st.markdown(f"**Skills Used:** {row['skills']}")

    def configure_skills_chart(self):
        st.header("🛠️ Skills")
        skills = self.data["key_skills"].dropna().str.split(", ").explode().value_counts()
        st.bar_chart(skills)
    
    def run_streamlit_app(self):
        """Orchestrator to configure the whole streamlit app"""
        self.config_page()
        self.config_sidebar()
        self.config_main_page()
        self.config_employment_timeline()
        self.config_job_descriptions()
        self.configure_skills_chart()
