import pandas as pd
import logging


def clean_subjects(subjects):
    """Remove overly specific or irrelevant subjects and return a cleaned list."""

    if isinstance(subjects, (list, set)):  # Handle both sets and lists
        # Convert the set to a sorted list to ensure consistent order
        subjects_list = sorted(subjects)  

        # Convert the list to a single string with " | " separator
        subjects_str = " | ".join(subjects_list)

        # Remove quotes and commas, strip whitespace
        subjects_str = subjects_str.replace('"', '').replace(',', '').strip()

        # Convert to lowercase
        subjects_str = subjects_str.lower()

        # Split back into a list and filter
        filtered_subjects = []
        for sub in subjects_str.split(" | "):
            # Rule 1: Remove subjects with numbers, colons, or very long names
            if any(char.isdigit() for char in sub) or ":" in sub or len(sub) > 50:
                continue
            filtered_subjects.append(sub)

        # Keep only the top 5 most relevant subjects
        return filtered_subjects[:5] if filtered_subjects else ['Subject unknown']

    return ['Subject unknown']




def transform(raw_data):
    """
    Transform the extracted data to a useful pandas dataframe
    
    Args:
        raw_data (dict): The raw API response containing book data
    
    Returns:
        pd.DataFrame: A pandas dataframe containing the transformed data.
    """
    
    logging.info('Transforming data')
    transformed_data = []

    for book in raw_data:
        book_id = book.get('key', 'No Key').lstrip('/works/')
        title = book.get('title', 'No Title')
        author = book.get('author', ['Unknown author'])[0]
        
        # Ensure first_publish_year is an integer
        first_publish_year = book.get('first_publish_year')
        if first_publish_year is None or not isinstance(first_publish_year, int):
            first_publish_year = None
        
        description = book.get('description', 'Unknown')
        
        subjects = book.get('subjects', [])
        cleaned_subjects  = list(clean_subjects(subjects))
        
        cover_url = book.get('cover_image')
        avg_rating = book.get('average_rating', 'Unknown')
        num_reviews = book.get('num_reviews', 'Unknown')

        if title == 'No Title' or author == 'Unknown author':
            logging.warning(f"Missing required fields: title='{title}', author_name='{author}'")

        book_info = {
            'book_id': book_id,
            'title': title,
            'author': author,
            'first_publish_year': first_publish_year,
            'description': description,
            'subjects': cleaned_subjects,
            'cover_url': cover_url,
            'avg_rating': avg_rating,
            'num_reviews': num_reviews
        }
        
        transformed_data.append(book_info)

    logging.info('Data successfully transformed')
    return pd.DataFrame(transformed_data)
