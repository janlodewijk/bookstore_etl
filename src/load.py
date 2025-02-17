from sqlalchemy import create_engine, text, String
from sqlalchemy.dialects.postgresql import ARRAY
import pandas as pd
import logging

def load(transformed_data, user_name, password, host='localhost', port=5432, db_name='books'):
    """
    Load transformed data into PostgreSQL database, avoiding duplicates.

    Args:
        transformed_data (pd.DataFrame): The cleaned data to be loaded
        user_name (str): Database username
        password (str): Database password
        host (str, optional): Database host. Defaults to 'localhost'.
        port (int, optional): Database port. Defaults to 5432.
        db_name (str, optional): Database name. Defaults to 'books'.
    """
    
    try:
        engine = create_engine(f'postgresql://{user_name}:{password}@{host}:{port}/{db_name}')
        
        with engine.connect() as connection:
            logging.info('Loading data')
            
            # Ensure the 'book_id' column exists in DataFrame
            if 'book_id' not in transformed_data.columns:
                raise ValueError("The DataFrame does not contain a 'book_id' column. Cannot set as primary key")
            
            transformed_data['first_publish_year'] = pd.to_numeric(transformed_data['first_publish_year'], errors='coerce')
            
            # Before loading the data:
            transformed_data['subjects'] = transformed_data['subjects'].apply(lambda x: x if isinstance(x, list) else str(x).split(' | '))
            
            # Ensure the 'book_id' is unique per book    
            transformed_data.drop_duplicates(subset='book_id', inplace=True)
            
            # Load data to a temporary table first
            transformed_data.to_sql('books_temp', con=connection, if_exists='replace', index=False,
                        dtype={'subjects': ARRAY(String)})	
            
            # Use SQL to insert or update
            sql = text("""
                       INSERT INTO books (book_id, title, author, first_publish_year, description, subjects, cover_url, avg_rating, num_reviews)
                        SELECT 
                            book_id, 
                            title, 
                            author,
                            CASE
                                WHEN first_publish_year IS NULL THEN NULL
                                ELSE CAST(first_publish_year AS BIGINT)
                            END AS first_publish_year,
                            description,
                            ARRAY(SELECT unnest(subjects)::TEXT) AS subjects,  -- Ensure subjects are properly formatted as TEXT[]
                            cover_url, 
                            avg_rating, 
                            num_reviews 
                        FROM books_temp
                        ON CONFLICT (book_id) DO UPDATE SET
                            title = EXCLUDED.title,
                            author = EXCLUDED.author,
                            first_publish_year = EXCLUDED.first_publish_year,
                            description = EXCLUDED.description,
                            subjects = EXCLUDED.subjects,
                            cover_url = EXCLUDED.cover_url,
                            avg_rating = EXCLUDED.avg_rating,
                            num_reviews = EXCLUDED.num_reviews;
            """)
            with engine.begin() as connection:
                connection.execute(sql)
            
            logging.info('Data successfully loaded')
    
    except Exception as e:
        logging.error(f'Error occurred during loading process: {e}')

