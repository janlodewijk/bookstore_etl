import requests
import json

def fetch_book_metadata(work_id):
    """Fetch metadata for a book from Open Library API."""
    work_url = f"https://openlibrary.org/works/{work_id}.json"
    ratings_url = f"https://openlibrary.org/works/{work_id}/ratings.json"

    # Fetch book metadata
    metadata_response = requests.get(work_url)
    metadata = metadata_response.json() if metadata_response.status_code == 200 else {}

    # Fetch ratings
    ratings_response = requests.get(ratings_url)
    ratings = ratings_response.json() if ratings_response.status_code == 200 else {}

    return metadata, ratings

def display_metadata(work_id):
    """Display book metadata for inspection."""
    metadata, ratings = fetch_book_metadata(work_id)

    print("\n=== Book Metadata ===")
    print(json.dumps(metadata, indent=2))  # Pretty-print metadata

    print("\n=== Ratings ===")
    print(json.dumps(ratings, indent=2))  # Pretty-print ratings

# Example: Fetch and inspect metadata for "To Kill a Mockingbird"
work_id = "OL45804W"  # Replace with any Open Library work ID
display_metadata(work_id)
