from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging
import requests



logging.basicConfig(level=logging.INFO)


def make_request(url, proxies=None, stream=False, method='GET', headers=None, data=None, auth=None):
    """
    Makes a network request using the requests library, with optional proxy setup, streaming support, and retry mechanism.

    Returns:
    - response (requests.Response): The response from the server.
    """
    retries = 3
    backoff_factor = 0.3
    status_forcelist = (500, 502, 503, 504)
    session = requests.Session()

    # Configure retries
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )

    # Mount the HTTPAdapter to the session
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    if proxies:
        session.proxies = proxies

    try:
        response = session.request(
            method, url, headers=headers, data=data, auth=auth, stream=stream)
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        response = None

    return response
