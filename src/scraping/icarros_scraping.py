import datetime
from src.result.file_result import FileResult
from src.result.filter_result import FilterResult
from src.scraping.scraping import Scraping


def create_file_name():
    scraping_datetime = datetime.datetime.now().strftime("%d_%m_%Y-%H_%M")
    return f"icarros_search-{scraping_datetime}.html"


#Example of filter_query_param 
# "?ord=35&&sop=esc_2.1_-cid_9668.1_-rai_50.1_-prf_44000.1_-kmm_100000.1_-mar_14.1_-mod_1052.1_-cam_false.1_-ami_2011.1_-"
def assembly_site_url(filter_query_param, page_number):
    return f"{ICarrosScraping.SITE_URL}?pag={page_number}&{filter_query_param}"


class ICarrosScraping(Scraping):
    SITE_URL = "https://www.icarros.com.br/ache/listaanuncios.jsp"
    CAR_CARD_HTML_ELEMENT = "ul"
    CAR_CARD_CSS_ID = "cards-grid"
    CAR_RESULT_TITLE_HTML_ELEMENT = "span"
    CAR_RESULT_TITLE_CSS_CLASS = "title__onLight ids_textStyle_overline header-list__subtitle header-list__subtitle--block"
    CAR_PROGRESS_BAR_ELEMENT = "progress"
    CAR_PROGRESS_BAR_CSS_CLASS = "pagination__progress-bar"

    def __init__(self, search_filter_params, filter_result: FilterResult, file_result: FileResult):
        self.search_filter_params = search_filter_params
        self.filter_result = filter_result
        self.file_result = file_result

    def start_scraping(self):
        results = self.scraping_cars()
        if len(results) == 0:
            print("No result found ⊙﹏⊙∥")
            return

        self.write_results(create_file_name(), results)

    def scraping_cars(self):
        results = []
        first_page_search = self.search(assembly_site_url(self.search_filter_params, 1))

        search_title = self.get_title(first_page_search)
        results.insert(0, search_title)

        results.append(self.get_cards(first_page_search))
        max_page = self.get_max_page(first_page_search)
        results.extend([self.get_cards(self.scraping_car(page)) for page in range(2, max_page + 1)])
        return results

    def scraping_car(self, page_number):
        return self.search(assembly_site_url(page_number))

    def get_title(self, scraping_result):
        return self.filter_result.filter(scraping_result,
                                         ICarrosScraping.CAR_RESULT_TITLE_HTML_ELEMENT,
                                         {"class": ICarrosScraping.CAR_RESULT_TITLE_CSS_CLASS})

    def get_cards(self, scraping_result):
        return self.filter_result.filter(scraping_result,
                                         ICarrosScraping.CAR_CARD_HTML_ELEMENT,
                                         {"id": ICarrosScraping.CAR_CARD_CSS_ID})

    def get_max_page(self, scraping_result):
        filtered_item = self.filter_result.filter(scraping_result,
                                                  ICarrosScraping.CAR_PROGRESS_BAR_ELEMENT,
                                                  {"class": ICarrosScraping.CAR_PROGRESS_BAR_CSS_CLASS})
        return int(filtered_item.attrs["max"])

    def write_results(self, file_name, results):
        for result in results:
            self.file_result.write(file_name, result.prettify())
