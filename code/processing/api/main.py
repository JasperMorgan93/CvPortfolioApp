from fastapi import FastAPI
from supabase import create_client, Client

app = FastAPI()

SUPABASE_URL = "https://dwltfqckbnzrlbvzhdha.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3bHRmcWNrYm56cmxidnpoZGhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzNjQ4NDEsImV4cCI6MjA1ODk0MDg0MX0.oxQUzlPCazMgXSQKNck-S03NXt-uvc36yjCpHvFOyy8"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/api/employment_history")
def get_employment_history():
    emp_history_json = supabase.table("employment_history").select("*").execute()
    return emp_history_json.data

@app.get("/api/users")
def get_users():
    users_json = supabase.table("users").select("*").execute()
    return users_json.data
