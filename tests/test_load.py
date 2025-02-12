import pandas as pd
from unittest import mock
from sqlalchemy.engine import Engine
from src.load import load

@mock.patch('src.load.create_engine')
def test_load(mock_create_engine):
    # Create a mock engine
    mock_engine = mock.Mock(spec=Engine)
    mock_create_engine.return_value = mock_engine

    # Create a mock connection with proper context manager setup
    mock_conn = mock.Mock()
    mock_context = mock.Mock()
    mock_context.__enter__ = mock.Mock(return_value=mock_conn)
    mock_context.__exit__ = mock.Mock(return_value=None)
    mock_engine.connect.return_value = mock_context

    # Mock DataFrame (transformed data)
    test_data = pd.DataFrame({
        'title': ['The mock revolt', 'To kill a mockingbird'],
        'author': ['Vera Cleaver', 'Harper Lee'],
        'first_publish_year': [1971, 1966],
        'edition_count': [5, 10]
    })

    # Call the load function
    load(test_data, 'test_user', 'test_password', 'localhost', 5432, 'test_db')

    # Verify create_engine was called correctly
    mock_create_engine.assert_called_once_with('postgresql://test_user:test_password@localhost:5432/test_db')

    # Verify connection was used
    mock_engine.connect.assert_called_once()