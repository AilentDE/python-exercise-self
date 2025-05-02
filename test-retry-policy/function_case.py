from tenacity import (
    retry,
    stop_after_attempt,
    stop_after_delay,
    wait_fixed,
    wait_random,
    wait_exponential,
)
from requests import get as http_get
from requests.exceptions import RequestException
from loguru import logger
from typing import Any
import time


class FunctionCase:
    """
    A class that implements a retry mechanism for function calls.
    """

    retry_policy = retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=3),
        reraise=True,
    )

    def __init__(self) -> None:
        """Initialize the FunctionCase class."""
        super().__init__()

    class StopPolicy:
        @staticmethod
        def stop_after_attempt(times: int = 3):
            return stop_after_attempt(times)

        @staticmethod
        def stop_after_delay(seconds: int = 10):
            return stop_after_delay(seconds)

    class WaitPolicy:
        @staticmethod
        def wait_seconds(seconds: int = 3):
            return wait_fixed(seconds)

        @staticmethod
        def wait_random(min_seconds: int = 1, max_seconds: int = 5):
            return wait_random(min=min_seconds, max=max_seconds)

        @staticmethod
        def wait_exponential(multiplier: int = 2, min_seconds: int = 1, max_seconds: int = 10):
            return wait_exponential(multiplier=multiplier, min=min_seconds, max=max_seconds)

    @retry_policy
    def try_request(self, url: str, **kwargs: Any):
        """
        Make an HTTP GET request with retry policy.

        Args:
            url (str): The URL to send the GET request to.
            kwargs: Additional arguments to pass to the request.

        Returns:
            Response: The response object from the GET request.
        """

        def _get():
            logger.debug(f"Trying to get URL: {url}")
            response = http_get(url, **kwargs)
            response.raise_for_status()
            return response

        return _get()


if __name__ == "__main__":
    # Example usage
    logger.info("FunctionCase example start")
    url = 'https://httpbin.org/status/500'
    function_case = FunctionCase()
    start = time.time()
    try:
        response = function_case.try_request(url, timeout=10)
        response.raise_for_status()
        logger.success(response.status_code)
    except RequestException as e:
        logger.error(f"Request failed: {e}")
    except Exception as ex:
        logger.critical(f"An unexpected error occurred: {ex}")
    finally:
        end = time.time()
    logger.info(f"FunctionCase example end: {end - start:.2f} seconds")
