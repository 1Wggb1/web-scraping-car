import requests
import datetime
from bs4 import BeautifulSoup

    
class Scraping:

    def search(self, site_url):
        scraping_content = requests.get(site_url).content
        return scraping_content
    
class FilterResult:
    
    def filter(self, scraping_result, html_filter_element, html_filter):
        soup_html_result = BeautifulSoup(scraping_result, 'html.parser')
        return soup_html_result.find(html_filter_element, html_filter)
    
class FileResult:
    
    def write(self, file_name: str, content: str):
        with open(file_name, "a", encoding="utf-8") as file:
             print("Writing file result")
             file.write(content)
            
class ICarrosScraping:
    
    def __init__(self, scraping: Scraping, filter_result: FilterResult, file_result: FileResult):
        self.scraping = scraping
        self.filter_result = filter_result
        self.file_result = file_result
    
    def start_scraping(self):
        results = self.scraping_cars()
        if len(results) == 0:
            print("No result found ⊙﹏⊙∥")
            return
        
        self.write_results(self.create_file_name(), results)
        
    def scraping_cars(self):
        results = []
        first_page_search = self.scraping.search(self.assembly_site_url(1))
        
        search_title = self.get_title(first_page_search)
        results.insert(0, search_title)
        
        results.append(self.get_cards(first_page_search))
        max_page = self.get_max_page(first_page_search)
        results.extend([self.get_cards(self.scraping_car(page)) for page in range(2, max_page + 1)])
        return results
    
    def scraping_car(self, page_number):
        return self.scraping.search(self.assembly_site_url(page_number))

    def create_file_name(self):
        scraping_datetime = datetime.datetime.now().strftime("%d_%m_%Y-%H_%M")
        return f"icarros_search-{scraping_datetime}.html"    
    
    def assembly_site_url(self, page_number):
        return f"https://www.icarros.com.br/ache/listaanuncios.jsp?pag={page_number}&ord=35&&sop=esc_2.1_-cid_9668.1_-rai_50.1_-prf_44000.1_-kmm_100000.1_-mar_14.1_-mod_1052.1_-cam_false.1_-ami_2011.1_-"
    
    def get_title(self, scraping_result):
        return self.filter_result.filter(scraping_result,
                                  "span",
                                  {"class": "title__onLight ids_textStyle_overline header-list__subtitle header-list__subtitle--block"})
    
    def get_cards(self, scraping_result):
        return self.filter_result.filter(scraping_result,"ul",{"id": "cards-grid"})
    
    def get_max_page(self, scraping_result):
        filtered_item = self.filter_result.filter(scraping_result, 
                                                  "progress", 
                                                  {"class": "pagination__progress-bar"})
        return int(filtered_item.attrs["max"])

    def write_results(self, file_name, results):
        for result in results:
            self.file_result.write(file_name, result.prettify())

if __name__ == "__main__":
    scraping = Scraping()
    filter_result = FilterResult()
    file_result = FileResult()
    icarros_scraping = ICarrosScraping(scraping, filter_result, file_result)
    icarros_scraping.start_scraping()
    