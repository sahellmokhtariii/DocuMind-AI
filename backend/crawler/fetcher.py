import requests

from backend.core.config import settings


class WebFetcher:
    """
    Download HTML pages.
    """

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": settings.USER_AGENT,
            }
        )

    def fetch(self, url: str):

        response = self.session.get(
            url,
            timeout=settings.REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return {
            "url": url,
            "status_code": response.status_code,
            "content_type": response.headers.get(
                "Content-Type",
                ""
            ),
            "html": response.text,
        }