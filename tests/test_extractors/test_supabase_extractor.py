import pytest
from unittest.mock import patch, MagicMock
from processing.extract.supabase_extractor import ExtractSupabaseProcessor


@patch("processing.extract.supabase_extractor.requests.get")
def test_validate_data_success_with_requests(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": 1, "name": "Alice"}]
    mock_get.return_value = mock_response

    extractor = ExtractSupabaseProcessor(
        base_url="https://fake.supabase.co", api_key="FAKE_KEY"
    )
    data = extractor.extract("dummy_endpoint")

    assert extractor.validate_data(data) == True


def test_validate_data_failure():
    extractor = ExtractSupabaseProcessor(base_url="", api_key="")
    with pytest.raises(ValueError, match="No data extracted"):
        extractor.validate_data([])
