import logging
import os


def setup_logger(log_file_path='logs/etl.log'):
    '''
    Configures logging for the ETL pipeline.
    
    Args:
        log_file_path (str): Path to the lof file
    '''
    
    # Make sure the logs directory exists
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        filename=log_file_path,
        filemode='a',    # Append mode
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    
    # Add a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    
    # Get the root logger and add the console handler
    logger = logging.getLogger()
    logger.addHandler(console_handler)
    