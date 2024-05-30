import requests


class Scraping:

    def search(self, site_url):
        scraping_content = requests.get(site_url).content
        return scraping_content
