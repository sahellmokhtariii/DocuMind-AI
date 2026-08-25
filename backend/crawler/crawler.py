from collections import deque
from urllib.parse import urljoin, urlparse
import json
from pathlib import Path

from backend.core.config import settings
from backend.core.logger import app_logger
from backend.crawler.fetcher import WebFetcher
from backend.crawler.parser import HTMLParser


class DocumentationCrawler:
    """
    BFS Documentation Crawler
    """

    def __init__(self):

        self.fetcher = WebFetcher()
        self.parser = HTMLParser()

        self.visited = set()

        self.documents = []

    # ----------------------------------------------------
    # Internal links only
    # ----------------------------------------------------

    def is_internal_link(self, url: str, base_domain: str):

        try:

            parsed = urlparse(url)

            if parsed.scheme not in ("http", "https"):
                return False

            return parsed.netloc == base_domain

        except Exception:
            return False

    # ----------------------------------------------------
    # Extract links
    # ----------------------------------------------------

    def extract_links(self, html: str, current_url: str):

        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "lxml")

        links = set()

        base_domain = urlparse(current_url).netloc
        root_prefix = "https://docs.python.org/3/"

        for tag in soup.find_all("a", href=True):

            href = tag["href"].strip()

            if href.startswith("#"):
                continue

            if href.startswith("mailto:"):
                continue

            if href.startswith("javascript:"):
                continue

            absolute = urljoin(current_url, href)

            absolute = absolute.split("#")[0]

            if not self.is_internal_link(absolute, base_domain):
                continue

            if not absolute.startswith(root_prefix):
                continue

            if absolute.endswith((
                ".pdf",
                ".zip",
                ".tar.gz",
                ".bz2",
                ".epub",
                ".txt",
                ".json",
                ".xml",
                ".png",
                ".jpg",
                ".jpeg",
                ".svg",
                ".gif",
            )):
                continue

            links.add(absolute)

        return sorted(links)

    # ----------------------------------------------------
    # Crawl one page
    # ----------------------------------------------------

    def crawl_page(self, url: str):

        app_logger.info(f"Crawling: {url}")

        response = self.fetcher.fetch(url)

        if response is None:
            return []

        html = response["html"]

        document = self.parser.parse(html, url)

        document["status_code"] = response["status_code"]
        document["content_type"] = response["content_type"]
        document["text_length"] = len(document["text"])

        self.documents.append(document)

        return self.extract_links(html, url)
        # ----------------------------------------------------
    # BFS Crawl
    # ----------------------------------------------------

    def crawl(
        self,
        start_url: str,
        max_pages: int = settings.MAX_PAGES,
        max_depth: int = settings.MAX_DEPTH,
    ):

        self.visited.clear()
        self.documents.clear()

        queue = deque()

        queue.append(
            (
                start_url,
                0,
            )
        )

        while queue and len(self.documents) < max_pages:

            current_url, depth = queue.popleft()

            if current_url in self.visited:
                continue

            self.visited.add(current_url)

            app_logger.info(
                f"[{len(self.documents)+1}/{max_pages}] {current_url}"
            )

            try:

                links = self.crawl_page(current_url)

            except Exception as e:

                app_logger.error(e)

                continue

            if depth >= max_depth:
                continue

            for link in links:

                if link not in self.visited:

                    queue.append(
                        (
                            link,
                            depth + 1,
                        )
                    )

        app_logger.success(
            f"Crawled {len(self.documents)} pages."
        )

        return self.documents

        # ----------------------------------------------------
    # Save JSON
    # ----------------------------------------------------

    def save(self, output_file):

        output_file = Path(output_file)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                self.documents,
                f,
                ensure_ascii=False,
                indent=2,
            )

        app_logger.success(
            f"Saved {len(self.documents)} pages -> {output_file}"
        )

    # ----------------------------------------------------
    # Crawl all documentation websites
    # ----------------------------------------------------

    def crawl_all(self):

        for name, url in settings.DOC_SITES.items():

            app_logger.info(f"Start crawling: {name}")

            self.crawl(url)

            output_file = (
                settings.RAW_DATA_DIR
                / f"{name}_docs.json"
            )

            self.save(output_file)

            app_logger.success(
                f"{name} finished."
            )

    def crawl_and_save(
            self,
            start_url: str,
            output_path,
            max_pages=settings.MAX_PAGES,
            max_depth=settings.MAX_DEPTH,
    ):               

        self.crawl(
            start_url=start_url,
            max_pages=max_pages,
            max_depth=max_depth,
        )

        self.save(output_path)