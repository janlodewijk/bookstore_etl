from unittest import mock
from src.extract import extract
import os

print(f'Current working direcory: {os.getcwd()}')

@mock.patch('requests.get')  # Mock the requests.get function
def test_extract(mock_get):
    mock_response = mock.Mock()
    mock_response.json.return_value ={
        'docs': [
            {'title': 'The mock revolt', 'author_name': ['Vera Cleaver'], 'first_publish_year': 1971},
            {'title': 'To kill a mockingbird', 'author_name': ['Harper Lee'], 'first_publish_year': 1966}            
        ]
    }
    mock_get.return_value = mock_response
    
    dummy_url = 'https://example.com/api'
    
    # Now call the extract function and assert it behaves as expected
    result = extract(dummy_url)
    assert len(result['docs']) == 2
    assert result['docs'][0]['title'] == 'The mock revolt'
    assert result['docs'][1]['author_name'] == ['Harper Lee']