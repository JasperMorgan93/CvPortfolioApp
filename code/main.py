from processing.extract.api_extractor import ExtractSupabaseProcessor

SUPABASE_URL = "https://dwltfqckbnzrlbvzhdha.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3bHRmcWNrYm56cmxidnpoZGhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzNjQ4NDEsImV4cCI6MjA1ODk0MDg0MX0.oxQUzlPCazMgXSQKNck-S03NXt-uvc36yjCpHvFOyy8"


supabase_extractor = ExtractSupabaseProcessor(base_url=SUPABASE_URL, api_key=SUPABASE_KEY)

emp_hist_df = supabase_extractor.extract("employment_history")
users_df = supabase_extractor.extract("users")

print("emp_hist_df")
print(emp_hist_df)
print("users_df")
print(users_df)