import tempfile
import csv
import os
import pytest
from ingest_daily import get_next_timestamp, fetch_data
from unittest.mock import patch



def test_get_next_timestamp_returns_correct_next_hour():
    
    # Arrange
    with tempfile.NamedTemporaryFile(mode="w",suffix=".csv",delete=False,newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['period','value'])
        writer.writerow(['2026-06-05T10','51000'])
        temp_path = f.name
    
    try:
        #Act
        result = get_next_timestamp(temp_path)

        #Assert
        assert result == "2026-06-05T11"
    finally:
        os.unlink(temp_path)
    

def test_get_next_timestamp_empty_csv_raises_error():

    #Arrange csv with only header and no data
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['period','value'])
        temp_path = f.name

    try:
        #Act and Assert
        with pytest.raises(IndexError):
            get_next_timestamp(temp_path)
    finally:
        os.unlink(temp_path)


def test_fetch_data_returns_api_response():

    #Arrange
    fake_response = {
        'response': {
            'data' : [
                {'period': '2026-06-05T10', 'value' : '51000'},
                {'period': '2026-06-05T11', 'value' : '52000'},
            ]
        }
    }

    with patch('ingest_daily.requests.get') as mock_get:
        mock_get.return_value.json.return_value = fake_response

        #Act
        result = fetch_data("2026-06-05T10")

    #Assert 
    assert result['response']['data'][0]['period'] == '2026-06-05T10'
    assert result['response']['data'][0]['value'] == '51000'