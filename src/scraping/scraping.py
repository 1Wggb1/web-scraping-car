import requests
from bs4 import BeautifulSoup


class Scraping:

    def search(self, site_url):
        scraping_content = requests.get(site_url).content
        return scraping_content

    def filter(self, scraping_result, html_filter_element, html_filter):
        soup_html_result = BeautifulSoup(scraping_result, 'html.parser')
        return soup_html_result.find(html_filter_element, html_filter)