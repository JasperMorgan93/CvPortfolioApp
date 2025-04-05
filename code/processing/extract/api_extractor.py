import requests
from typing import List, Dict, Any
from processing.extract.base import BaseExtractor

SUPABASE_URL = "https://dwltfqckbnzrlbvzhdha.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3bHRmcWNrYm56cmxidnpoZGhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzNjQ4NDEsImV4cCI6MjA1ODk0MDg0MX0.oxQUzlPCazMgXSQKNck-S03NXt-uvc36yjCpHvFOyy8"

class ExtractSupabaseProcessor(BaseExtractor):
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def extract(self, endpoint) -> List[Dict[str, Any]]:
        """Extract data from the Supabase database via the PostgREST API."""
        rest_endpoint = f"/rest/v1/{endpoint}"
        url = f"{self.base_url}{rest_endpoint}"
        return self._send_request(url)

    def _send_request(self, url: str) -> List[Dict[str, Any]]:
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()


supabase_extractor = ExtractSupabaseProcessor(base_url=SUPABASE_URL, api_key=SUPABASE_KEY)

data = supabase_extractor.extract()
print(data)