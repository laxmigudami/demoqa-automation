import requests

from config.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)
config = get_config()


class APIClient:
    """API Client for DEMOQA Book Store API"""

    # API Endpoints - centralized configuration
    ENDPOINT_BOOKS = "/Books"
    ENDPOINT_BOOK = "/Book"

    def __init__(self, base_url=None, timeout=None):
        """Initialize API Client

        Args:
            base_url: API base URL
            timeout: Request timeout in seconds
        """
        self.base_url = base_url or config.API_BASE_URL
        self.timeout = timeout or config.EXPLICIT_WAIT
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        logger.info(f"APIClient initialized with base_url: {self.base_url}")

    def get_books(self):
        """Get all books from the API

        Returns:
            dict: Response containing 'books' array, or empty dict on error
        """
        try:
            url = f"{self.base_url}{self.ENDPOINT_BOOKS}"
            logger.debug(f"Fetching books from: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully fetched {len(data.get('books', []))} books")
            return data
        except requests.Timeout as e:
            logger.error(f"Timeout while fetching books: {e}")
            return {"books": []}
        except requests.HTTPError as e:
            logger.error(f"HTTP error fetching books (Status {e.response.status_code}): {e}")
            return {"books": []}
        except requests.RequestException as e:
            logger.error(f"Request error fetching books: {e}")
            return {"books": []}
        except (ValueError, KeyError) as e:
            logger.error(f"Error parsing books response: {e}")
            return {"books": []}

    def get_book_by_isbn(self, isbn):
        """Get a specific book by ISBN

        Args:
            isbn: Book ISBN number

        Returns:
            dict: Book details, or empty dict on error
        """
        try:
            url = f"{self.base_url}{self.ENDPOINT_BOOK}"
            params = {"ISBN": isbn}
            logger.debug(f"Fetching book with ISBN {isbn} from: {url}")
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully fetched book: {data.get('title', 'Unknown')}")
            return data
        except requests.Timeout as e:
            logger.error(f"Timeout while fetching book {isbn}: {e}")
            return {}
        except requests.HTTPError as e:
            logger.error(f"HTTP error fetching book {isbn} (Status {e.response.status_code}): {e}")
            return {}
        except requests.RequestException as e:
            logger.error(f"Request error fetching book {isbn}: {e}")
            return {}
        except (ValueError, KeyError) as e:
            logger.error(f"Error parsing book {isbn} response: {e}")
            return {}

    def close(self):
        """Close the session and cleanup resources"""
        if self.session:
            self.session.close()
            logger.debug("API session closed")
