# Bookstore ETL

-- Under construction --

## Project Overview
Bookstore ETL is a data pipeline that extracts book metadata from the Open Library API, transforms it for relevance, and loads it into a PostgreSQL database. The goal is to develop a personalized book recommendation system based on user preferences.

## Features
- **Extract**: Retrieves book metadata from the Open Library API.
- **Transform**: Cleans and enriches the data by processing publication years, genres, and other metadata.
- **Load**: Stores the structured data in a PostgreSQL database.
- **Scoring System**:
  - Subject Matching (40%)
  - Ratings & Popularity (30%)
  - Text Similarity (30%)
- **Testing**: Unit tests implemented using `pytest`.

## Technologies Used
- **Python** (ETL logic and API interactions)
- **PostgreSQL** (Database storage)
- **SQLAlchemy** (Database connection)
- **pandas** (Data transformation)
- **pytest** (Testing framework)
- **Logging** (Monitoring ETL processes)

## Project Structure
```
bookstore_etl/
│── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── utils.py
│   ├── main.py
│── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   ├── test_load.py
│── logs/
│   ├── etl.log
│── requirements.txt
│── README.md
│── .gitignore
```

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/janlodewijk/bookstore_etl.git
   ```
2. Navigate to the project directory:
   ```sh
   cd bookstore_etl
   ```
3. Create a virtual environment:
   ```sh
   python -m venv venv
   ```
4. Activate the virtual environment:
   - Windows:
     ```sh
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```sh
     source venv/bin/activate
     ```
5. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
Run the ETL pipeline with:
```sh
python src/main.py
```

## Environment Variables
Create a `.env` file to store API keys and database credentials:
```
OPEN_LIBRARY_API_KEY=your_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/bookstore
```

## Testing
Run tests using:
```sh
pytest tests/
```

## Future Improvements
- Enhance the recommendation algorithm.
- Implement a front-end interface.
- Deploy the system for broader use.

## License
This project is licensed under the MIT License.

