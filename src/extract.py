import requests
import logging


def extract(url, q='Python', limit=10):
    """
    Extract data from the Open Library API.

    Args:
        url (str): The base URL of the API.
        q (str): Search term for querying books. Defaults to 'Python' if not provided.
        limit (int, optional): Number of results to limit. Defaults to 10.

    Returns:
        list: A list of the extracted book data.
    """
    logging.info('Extraction has started')
    
    # Construct query parameters
    params = {'q': q, 'limit': limit}

    try:
        # Make the GET request with the query parameters
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        logging.info('Succesful API request')

        # Parse the JSON response and retrieve the keys        
        raw_data = response.json()
        extracted_data = []
        
        # Loop through the books and extract relevant information
        for book in raw_data.get('docs', []):
            key = book.get('key', 'Unknown')
            title = book.get('title', 'Unknown')
            author = book.get('author_name', ['Unknown'])
            first_publish_year = book.get('first_publish_year', None)
            if first_publish_year == "Unknown":
                first_publish_year = None
            if first_publish_year != None and not isinstance(first_publish_year, int):
                try:
                    first_publish_year = int(first_publish_year)
                except ValueError:
                    first_publish_year = None
            
            # Log the first publish year value for debugging
            logging.debug(f"First publish year for {title}: {first_publish_year}")
            
            book_info = {'key': key,
                         'title': title,
                         'author': author,
                         'first_publish_year': first_publish_year}
            
            extracted_data.append(book_info)
        
        for book in extracted_data:
            key = book['key']
            url_2 = f'https://openlibrary.org/{key}.json'
            
            try:
                response_2 = requests.get(url_2)
                response_2.raise_for_status()
                logging.info(f'Succesfully fetched data for {key}')
                
                # Parse the JSON response and retrieve the keys
                book_metadata = response_2.json()
                
                # Extract additional details
                description = book_metadata.get('description', 'No description available')
                if isinstance(description, dict):
                    description = description.get('value', 'No description available')
                subjects = book_metadata.get('subjects', [])

                                # Add this information to the book dictionary
                book['description'] = description
                book['subjects'] = subjects
                
                covers = book_metadata.get('covers')
                
                if covers and isinstance(covers, list):
                    cover_id = covers[0]
                    book['cover_image'] = f'https://covers.openlibrary.org/b/id/{cover_id}-L.jpg'
                else:
                    book['cover_image'] = None
         
                
                ratings_url = f'https://openlibrary.org/{key}/ratings.json'
                try:
                    response_3 = requests.get(ratings_url)
                    response_3.raise_for_status()
                    ratings_data = response_3.json()
                    
                    average_rating = ratings_data.get('summary', {}).get('average')
                    book['average_rating'] = round(average_rating, 2) if average_rating else None
                    book['num_reviews'] = ratings_data.get('summary', {}).get('count', 0)
                
                except requests.exceptions.RequestException as e:
                    logging.error(f"Error occurred while fetching ratings for {key}: {e}")
                    book['average_rating'] = None
                    book['num_reviews'] = 0
            
            except requests.exceptions.RequestException as e:
                logging.error(f"Error occurred while fetching metadata for {key}: {e}")
                continue
            
        logging.info('Extraction has finished')
        return extracted_data
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred during API request: {e}")
        return None
    
