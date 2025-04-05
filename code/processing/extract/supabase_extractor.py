import requests
from typing import List, Dict, Any
from processing.extract.base import BaseExtractor

class ExtractSupabaseProcessor(BaseExtractor):
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json"
        }

    def extract(self, endpoint) -> List[Dict[str, Any]]:
        """Extract data from the Supabase database via the PostgREST API."""
        rest_endpoint = f"/rest/v1/{endpoint}"
        url = f"{self.base_url}{rest_endpoint}?apikey={self.api_key}"
        return self._send_request(url)

    def _send_request(self, url: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code}")
                print(f"Response Text: {response.text}")
                response.raise_for_status()
        
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            raise

    def validate_data(self, data: List[Dict[str, Any]]) -> bool:
        if not data:
            raise ValueError(f"No data extracted. Failing")
        return True