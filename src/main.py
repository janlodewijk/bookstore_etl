from utils import setup_logger
import logging
from extract import extract
from transform import transform
from dotenv import load_dotenv
import os
from load import load

load_dotenv()

user_name = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "books")

if __name__ == '__main__':
    setup_logger()
    logging.info('ETL pipeline started.')
    

url = 'https://openlibrary.org/search.json'
q='tolstoy'

raw_data = extract(url=url, q=q, limit=10)

transformed_data = transform(raw_data)
print(transformed_data['subjects'].dtype)

load(transformed_data, user_name, password)