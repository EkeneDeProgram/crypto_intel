import requests
from requests.exceptions import RequestException
import time
import logging

logger = logging.getLogger(__name__)

def get_json(url: str, params: dict = None, retries: int = 3, timeout: int = 10):
    """
    Fetch JSON data from a URL with retry and error handling.

    Args:
        url (str): API endpoint.
        params (dict, optional): Query parameters.
        retries (int): Number of retry attempts.
        timeout (int): Request timeout in seconds.

    Returns:
        dict: JSON response.

    Raises:
        Exception: If all retries fail.
    """
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()  # HTTP errors
            return response.json()
        except RequestException as e:
            logger.warning(f"Attempt {attempt} failed for URL {url}: {e}")
            if attempt < retries:
                time.sleep(2 ** attempt)  # exponential backoff
            else:
                logger.error(f"All {retries} attempts failed for URL {url}")
                raise
