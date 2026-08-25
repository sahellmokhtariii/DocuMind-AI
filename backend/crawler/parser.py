from bs4 import BeautifulSoup


class HTMLParser:
    """
    Extract only the main readable content from documentation pages.
    """

    @staticmethod
    def extract_title(html: str) -> str:

        soup = BeautifulSoup(html, "lxml")

        if soup.title and soup.title.string:
            return soup.title.string.strip()

        h1 = soup.find("h1")
        if h1:
            return h1.get_text(" ", strip=True)

        return "Untitled"

    @staticmethod
    def extract_text(html: str) -> str:

        soup = BeautifulSoup(html, "lxml")

        # ---------------------------------------------------
        # remove useless tags
        # ---------------------------------------------------

        for tag in soup([
            "script",
            "style",
            "noscript",
            "svg",
            "header",
            "footer",
            "nav",
            "aside",
            "form",
            "button",
        ]):
            tag.decompose()

        # ---------------------------------------------------
        # Python docs main content
        # ---------------------------------------------------

        main = (
            soup.find("article")
            or soup.find(role="main")
            or soup.find("main")
            or soup.find(class_="document")
            or soup.find(class_="body")
            or soup.body
        )

        if main is None:
            main = soup

        text = main.get_text(separator=" ", strip=True)

        # ---------------------------------------------------
        # clean lines
        # ---------------------------------------------------

        blacklist = {
            "Navigation",
            "Theme",
            "Light",
            "Dark",
            "Auto",
            "Toggle",
            "Search",
            "Index",
            "Modules",
            "Previous topic",
            "Next topic",
            "Contents",
            "Donate",
            "This page",
            "|",
            "»",
            "Python »",
        }

        cleaned = []

        for line in text.splitlines():

            line = " ".join(line.split()).strip()

            if not line:
                continue

            if len(line) < 4:
                continue

            if line in blacklist:
                continue

            cleaned.append(line)

        return "\n".join(cleaned)

    # ==========================================================
    # NEW METHODS
    # ==========================================================

    def parse(self, html: str, url: str) -> dict:
        """
        Parse HTML and return structured document.

        Args:
            html: HTML content
            url: Page URL

        Returns:
            Dictionary with title, url, and text
        """

        title = self.extract_title(html)
        text = self.extract_text(html)

        return {
            "title": title,
            "url": url,
            "text": text,
        }

    def save_json(self, documents: list, output_path: str) -> None:
        """
        Save documents to JSON file.
        """

        import json

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(
                documents,
                f,
                ensure_ascii=False,
                indent=2,
            )

    def load_json(self, input_path: str) -> list:
        """
        Load documents from JSON file.
        """

        import json

        with open(input_path, "r", encoding="utf-8") as f:
            return json.load(f)