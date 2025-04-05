from processing.extract.api_extractor import ExtractSupabaseProcessor
import pandas as pd

SUPABASE_URL = "https://dwltfqckbnzrlbvzhdha.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3bHRmcWNrYm56cmxidnpoZGhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzNjQ4NDEsImV4cCI6MjA1ODk0MDg0MX0.oxQUzlPCazMgXSQKNck-S03NXt-uvc36yjCpHvFOyy8"


supabase_extractor = ExtractSupabaseProcessor(base_url=SUPABASE_URL, api_key=SUPABASE_KEY)

emp_hist_df = pd.DataFrame(supabase_extractor.extract("employment_history"))
users_df = pd.DataFrame(supabase_extractor.extract("users"))

user_emp_df = pd.merge(
    users_df, 
    emp_hist_df, 
    left_on='id', 
    right_on='users_id',
    suffixes=('_users', '_emp')
    )

print("user_emp_df")
print(user_emp_df)