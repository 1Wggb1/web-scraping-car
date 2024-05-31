from src.result.file_result import FileResult
from src.result.file_result_repository import FileResultRepository
from src.scraping.scraping import Scraping
from src.util.logger_util import log


#Example of filter_query_param 
# "ord=35&&sop=esc_2.1_-cid_9668.1_-rai_50.1_-prf_44000.1_-kmm_100000.1_-mar_14.1_-mod_1052.1_-cam_false.1_-ami_2011.1_-"
def _assembly_site_url(page_number, filter_query_params):
    return f"{ICarrosScraping.SITE_URL}?pag={page_number}&{filter_query_params}"


class ICarrosScraping(Scraping, FileResult):
    SITE_URL = "https://www.icarros.com.br/ache/listaanuncios.jsp"
    CAR_CARD_HTML_ELEMENT = "ul"
    CAR_CARD_CSS_ID = "cards-grid"
    CAR_RESULT_TITLE_HTML_ELEMENT = "span"
    CAR_RESULT_TITLE_CSS_CLASS = "title__onLight ids_textStyle_overline header-list__subtitle header-list__subtitle--block"
    CAR_PROGRESS_BAR_ELEMENT = "progress"
    CAR_PROGRESS_BAR_CSS_CLASS = "pagination__progress-bar"
    RESULT_FOLDER_NAME = "icarros"
    RESULT_FILE_EXTENSION = "html"
    REPOSITORY_FILE_NAME = "/icarros/found_results.json"

    def __init__(self, filter_query_params):
        self.filter_query_params = filter_query_params
        self.file_result = FileResult()
        self.repository = FileResultRepository(ICarrosScraping.REPOSITORY_FILE_NAME, self.file_result)

    def start_car_scraping(self):
        log.info("Starting icarros scraping...")
        first_page_search = self.do_car_search(1)
        if not len(first_page_search):
            log.info("No result found on icarros scraping ⊙﹏⊙∥")
            return
        log.info("Icarros scraping result...")
        self.do_cars_scraping(first_page_search)

    def do_car_search(self, page_number):
        return self.search(_assembly_site_url(page_number, self.filter_query_params))

    def do_cars_scraping(self, first_page_search):
        html_scraping_results = []

        title = self.get_title(first_page_search)
        html_scraping_results.insert(0, title)

        car_cards = self.get_car_cards(first_page_search)
        html_scraping_results.append(car_cards)

        ads_data = self.extract_ads_data(car_cards)
        max_page = self.get_max_page(first_page_search)
        for page in range(2, max_page + 1):
            car_cards = self.get_car_cards(self.do_car_search(page))
            ads_data |= self.extract_ads_data(car_cards)
            html_scraping_results.append(car_cards)

        self.repository.merge(ads_data)
        self.persist_html_result(html_scraping_results)

    def get_title(self, scraping_result):
        return self.filter(scraping_result,
                           ICarrosScraping.CAR_RESULT_TITLE_HTML_ELEMENT,
                           {"class": ICarrosScraping.CAR_RESULT_TITLE_CSS_CLASS})

    def get_car_cards(self, scraping_result):
        return self.filter(scraping_result,
                           ICarrosScraping.CAR_CARD_HTML_ELEMENT,
                           {"id": ICarrosScraping.CAR_CARD_CSS_ID})

    def extract_ads_data(self, car_cards):
        result = {}
        html_images = car_cards.findAll("img")
        for img in html_images:
            val = self.extract_onclick_value(img)
            key = self.extract_item_id(val)
            result[key] = val
        return result

    def extract_onclick_value(self, element):
        onclick_val = element.attrs["onclick"]
        onclick_val = onclick_val[onclick_val.index("(") + 1:]
        return onclick_val[:len(onclick_val) - 1]

    def extract_item_id(self, onclick_val):
        text_to_find = "item_id: "
        item_id_first_letter_idx = onclick_val.find(text_to_find)
        #+1 skip quotation mark
        item_id_start_idx_excluding_quotation = item_id_first_letter_idx + len(text_to_find) + 1
        #-1 skip quotation mark
        item_id_start_final_idx_diff = (onclick_val[item_id_start_idx_excluding_quotation:].find(",") - 1)
        item_id_final_idx = item_id_start_idx_excluding_quotation + item_id_start_final_idx_diff
        return onclick_val[item_id_start_idx_excluding_quotation:item_id_final_idx]

    def get_max_page(self, scraping_result):
        filtered_item = self.filter(scraping_result,
                                    ICarrosScraping.CAR_PROGRESS_BAR_ELEMENT,
                                    {"class": ICarrosScraping.CAR_PROGRESS_BAR_CSS_CLASS})
        return int(filtered_item.attrs["max"])

    def persist_html_result(self, results):
        log.info("Persisting html result file")
        self.repository.persist_all(results,
                                    ICarrosScraping.RESULT_FOLDER_NAME,
                                    ICarrosScraping.RESULT_FILE_EXTENSION)
