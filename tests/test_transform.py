import pytest
from src.transform import transform
import pandas as pd

def test_transform():
    # Create a sample DataFrame
    raw_data = {
        'docs': [
            {'title': 'The mock revolt', 'author_name': ['Vera Cleaver'], 'first_publish_year': 1971, 'edition_count': 1},
            {'title': 'To kill a mockingbird', 'author_name': ['Harper Lee'], 'first_publish_year': 1966, 'edition_count': 6} 
        ]
    }
    
    result_df = transform(raw_data)
    
    assert isinstance(result_df, pd.DataFrame)  # Check if the result is a DataFrame
    assert len(result_df) == 2  # Check if the DataFrame has the expected number of rows
    assert 'title' in result_df.columns  # Check if 'title' column exists
    assert result_df.iloc[0]['title'] == 'The mock revolt'  # Check if the first row has the expected title
    assert result_df.iloc[1]['author'] == 'Harper Lee'  # Check if the second row has the expected author name