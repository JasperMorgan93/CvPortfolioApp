import pandas as pd
import os
import sys
from processing.extract.supabase_extractor import ExtractSupabaseProcessor
from processing.transform.dataframe_transformations import DataFrameTransformer
from processing.loaders.streamlit.streamlit_utils import StreamlitProcessor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "processing")))

SUPABASE_URL = "https://dwltfqckbnzrlbvzhdha.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3bHRmcWNrYm56cmxidnpoZGhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzNjQ4NDEsImV4cCI6MjA1ODk0MDg0MX0.oxQUzlPCazMgXSQKNck-S03NXt-uvc36yjCpHvFOyy8"


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
