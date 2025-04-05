import streamlit as st
import pandas as pd

class StreamlitProcessor:

    data : pd.DataFrame
    app_name : str

    def __init__(self, data, app_name):
        self.data = data
        self.app_name = app_name

    def prepare_data(self):
        """_summary_

        Args:
            dataframe (_type_): _description_

        Returns:
            pd.DataFrame: _description_
        """
        self.data = self.data.sort_values(by="start_date", ascending=False)
    
    def create_streamlit_app(self):
        """WIP"""
        # ---- Page Config ----
        st.set_page_config(layout="wide", page_title="Data Engineering CV")

        # ---- Sidebar/Profile ----
        # st.sidebar.image("assets/images/profile_pic.jpg", width=150)
        st.sidebar.title("Jasper Morgan")
        st.sidebar.markdown("**Email:** jasper.morgan@hotmail.co.uk")
        st.sidebar.markdown(
            "**GitHub:** [JasperMorgan93](https://github.com/JasperMorgan93/CvPortfolioApp)"
        )
        st.sidebar.markdown(
            "**LinkedIn:** [Jasper Morgan](https://www.linkedin.com/in/jasper-morgan-185841165/)"
        )

        # ---- Main Page ----
        st.title("Data Engineering CV")
        st.markdown("""
                    A visual and interactive version of my CV/portfolio. 
                    The data are loaded from SQL via the supabase API, 
                    processed in Python and presented via Streamlit
                    """)

        # ---- Employment Timeline ----
        import plotly.express as px

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


        # ---- Job Descriptions ----
        st.header("📋 Job Descriptions")
        for idx, row in self.data.iterrows():
            st.subheader(f"{row['role']} - {row['company_name']}")
            st.caption(f"{row['start_date'].date()} → {row['end_date'].date()}")
            st.markdown(
                f"**Description:** {row.get('description', 'No description provided.')}"
            )
            if "skills" in row:
                st.markdown(f"**Skills Used:** {row['skills']}")

        # ---- Skills Cloud or Tags ----
        st.header("🛠️ Skills")
        skills = self.data["key_skills"].dropna().str.split(", ").explode().value_counts()
        st.bar_chart(skills)
