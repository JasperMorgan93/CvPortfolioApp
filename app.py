import pandas as pd
import os
from dotenv import load_dotenv
import streamlit as st
from processing.extract.supabase_extractor import ExtractSupabaseProcessor
from processing.transform.dataframe_transformations import DataFrameTransformer
from processing.loaders.streamlit.streamlit_utils import StreamlitProcessor

load_dotenv()

SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("Missing Supabase credentials.")


## -- Load data from supabase -- ##
supabase_extractor = ExtractSupabaseProcessor(
    base_url=SUPABASE_URL, api_key=SUPABASE_KEY
)

emp_hist_df = pd.DataFrame(supabase_extractor.extract("employment_history"))
users_df = pd.DataFrame(supabase_extractor.extract("users"))

## -- Process data -- ##

user_emp_df = pd.merge(
    users_df,
    emp_hist_df,
    left_on="id",
    right_on="users_id",
    suffixes=("_users", "_emp"),
)

data_transformer = DataFrameTransformer()
user_emp_df = data_transformer.fill_null_dates_with_today(user_emp_df, "end_date")
user_emp_df = data_transformer.set_date_columns_to_datetime(
    user_emp_df, ["start_date", "end_date"]
)

## -- Deploy to app -- ##
slt_loader = StreamlitProcessor(user_emp_df, "jm-data-engineer-cv-app")
slt_loader.prepare_data()
slt_loader.run_streamlit_app()
