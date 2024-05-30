from bs4 import BeautifulSoup


class FilterResult:

    def filter(self, scraping_result, html_filter_element, html_filter):
        soup_html_result = BeautifulSoup(scraping_result, 'html.parser')
        return soup_html_result.find(html_filter_element, html_filter)
