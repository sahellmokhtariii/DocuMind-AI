from backend.crawler.crawler import DocumentationCrawler

if __name__ == "__main__":
    crawler = DocumentationCrawler()
    
    # اجرای کراولینگ و ذخیره
    crawler.crawl_and_save(
        start_url="https://docs.python.org/3/",
        output_path="python_docs.json",
        max_pages=5
    )
    
    print("Done! Check python_docs.json")