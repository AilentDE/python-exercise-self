from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util.retry import Retry
from loguru import logger
import time


class LoggingRetry(Retry):
    def increment(self, *args, **kwargs):
        new_retry = super().increment(*args, **kwargs)
        wait = new_retry.get_backoff_time()
        logger.debug(
            f"Attempt {self.total - new_retry.total}/{self.total} - "
            f"Will wait {wait:.2f}s before retrying - "
            f"URL: {args[1] if len(args) > 1 else 'unknown'}"
        )
        return new_retry


class SessionCase(Session):
    """
    A subclass of requests.Session that implements a retry policy for HTTP requests.
    """

    def __init__(self, retries=3, backoff_factor=0.5, status_forcelist=None):
        """Initialize the SessionCase with a retry policy.

        Args:
            retries (int): The number of retries to allow.
            backoff_factor (float): A backoff factor to apply between attempts.
            status_forcelist (list): A list of HTTP status codes to retry on.
        """
        super().__init__()
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist or [500, 502, 503, 504]
        self.allowed_methods = ['HEAD', 'GET', 'OPTIONS', 'PUT', 'DELETE', 'TRACE', 'POST']
        self.mount('http://', HTTPAdapter(max_retries=self._get_retry()))
        self.mount('https://', HTTPAdapter(max_retries=self._get_retry()))

    def _get_retry(self):
        return LoggingRetry(
            total=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
            allowed_methods=self.allowed_methods,
        )


if __name__ == "__main__":
    # Example usage
    logger.info("SessionCase example start")
    session = SessionCase(retries=3, backoff_factor=1)
    start = time.time()
    try:
        response = session.get('https://httpbin.org/status/500', timeout=10)
        logger.success(response.status_code)
    except RequestException as e:
        logger.error(f"Request failed: {e}")
    except Exception as ex:
        logger.critical(f"An unexpected error occurred: {ex}")
    finally:
        end = time.time()
        session.close()
    logger.info(f"SessionCase example end: {end - start:.2f} seconds")
