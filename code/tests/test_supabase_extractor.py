import pytest
from processing.extract.supabase_extractor import ExtractSupabaseProcessor

def test_validate_data_success():
    extractor = ExtractSupabaseProcessor()
    data = extractor.extract()
    assert extractor.validate_data(data) == True