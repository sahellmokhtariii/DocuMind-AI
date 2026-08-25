def __init__(self, start_url: str, max_pages: int = 10):
    self.start_url = start_url
    self.max_pages = max_pages

    self.domain = urlparse(start_url).netloc

    self.visited: set[str] = set()
    self.queued: set[str] = {start_url}

    self.queue = deque([start_url])
    self.documents = []

    # Reuse HTTP connections
    self.session = requests.Session()
    self.session.headers.update(
        {
            "User-Agent": settings.USER_AGENT
        }
    )

    print("Session created:", hasattr(self, "session"))