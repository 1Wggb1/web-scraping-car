import requests
from bs4 import BeautifulSoup
from unidecode import unidecode


class Scraping:
    FAKE_AGENT_HEADER = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

    def search(self, site_url):
        scraping_content = requests.get(site_url, headers=Scraping.FAKE_AGENT_HEADER).content
        return scraping_content

    def filter(self, scraping_result, html_filter_element, html_filter):
        soup_html_result = BeautifulSoup(scraping_result, 'html.parser')
        return soup_html_result.find(html_filter_element, html_filter)

    def create_result(self, ad_url: str, result: str) -> dict:
        return {
            "ad_url": unidecode(ad_url),
            "car": result
        }