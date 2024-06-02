from src.result.file_result import FileResult
from src.result.file_result_repository import FileResultRepository
from src.scraping.scraping import Scraping
from src.util.logger_util import log
from typing import Final


class ICarrosScraping(Scraping, FileResult):
    MAIN_URL: Final = "https://www.icarros.com.br"
    SITE_URL: Final = f"{MAIN_URL}/ache/listaanuncios.jsp"
    CAR_CARD_HTML_ELEMENT: Final = "ul"
    CAR_CARD_CSS_ID: Final = "cards-grid"
    CAR_RESULT_TITLE_HTML_ELEMENT: Final = "span"
    CAR_RESULT_TITLE_CSS_CLASS: Final = "title__onLight ids_textStyle_overline header-list__subtitle header-list__subtitle--block"
    CAR_PROGRESS_BAR_ELEMENT: Final = "progress"
    CAR_PROGRESS_BAR_CSS_CLASS: Final = "pagination__progress-bar"
    RESULT_HTML_FILE_NAME: Final = "icarros_ads"
    RESULT_FOLDER_NAME: Final = "icarros"
    RESULT_FILE_EXTENSION: Final = "html"
    REPOSITORY_FILE_NAME: Final = "/icarros/found_results.json"

    def __init__(self, filter_query_params):
        self.filter_query_params = filter_query_params
        self.file_result = FileResult()
        self.repository = FileResultRepository(ICarrosScraping.REPOSITORY_FILE_NAME, self.file_result)

    def get_latest_cars(self):
        return self.repository.find_latest()

    def start_car_scraping(self):
        log.info("Starting icarros scraping...")
        first_page_search = self.do_car_search(1)
        if not len(first_page_search):
            log.info("No result found on icarros scraping ⊙﹏⊙∥")
            return
        log.info("Icarros scraping result...")
        self.do_cars_scraping(first_page_search)

    def do_car_search(self, page_number):
        return self.search(ICarrosScraping.__assembly_site_url(page_number, self.filter_query_params))

    #Example of filter_query_param 
    # "ord=35&&sop=esc_2.1_-cid_9668.1_-rai_50.1_-prf_44000.1_-kmm_100000.1_-mar_14.1_-mod_1052.1_-cam_false.1_-ami_2011.1_-"
    @staticmethod
    def __assembly_site_url(page_number, filter_query_params):
        return f"{ICarrosScraping.SITE_URL}?pag={page_number}&{filter_query_params}"

    def do_cars_scraping(self, first_page_search):
        title = self.get_title(first_page_search)
        html_scraping_results = title.__str__()

        car_cards = self.get_car_cards(first_page_search)
        html_scraping_results += car_cards.__str__()

        ads_data: dict = self.extract_ads_data(car_cards)
        max_page = self.get_max_page(first_page_search)
        self.do_scraping_on_pages(2, max_page, ads_data, html_scraping_results)

        self.repository.merge(ads_data)
        self.persist_html_result(html_scraping_results)

    def do_scraping_on_pages(self, start_page, max_page: int, ads_data: dict, html_scraping_results: str):
        for page in range(start_page, max_page + 1):
            car_cards = self.get_car_cards(self.do_car_search(page))
            ads_data |= ICarrosScraping.extract_ads_data(car_cards)
            html_scraping_results += car_cards.__str__()

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
        ads = car_cards.select(f"li.small-offer-card[data-anuncioid]")
        for ad in ads:
            ad_id = ad["data-anuncioid"]
            ad_url = ad.a["href"]
            result[ad_id] = self.create_result(
                f"{ICarrosScraping.MAIN_URL}{ad_url}",
                ICarrosScraping.extract_car_info(ad.img))
        return result

    @staticmethod
    def extract_car_info(element):
        onclick_val = element.attrs["onclick"]
        onclick_val = onclick_val[onclick_val.index("(") + 1:]
        return onclick_val[:len(onclick_val) - 1]

    def get_max_page(self, scraping_result):
        filtered_item = self.filter(scraping_result,
                                    ICarrosScraping.CAR_PROGRESS_BAR_ELEMENT,
                                    {"class": ICarrosScraping.CAR_PROGRESS_BAR_CSS_CLASS})
        return int(filtered_item.attrs["max"])

    def persist_html_result(self, results: str):
        log.info("Persisting html result file")
        self.repository.persist_all(results,
                                    ICarrosScraping.__create_file_name(
                                        ICarrosScraping.RESULT_FOLDER_NAME,
                                        ICarrosScraping.RESULT_HTML_FILE_NAME,
                                        ICarrosScraping.RESULT_FILE_EXTENSION))

    @staticmethod
    def __create_file_name(result_folder_name, file_name, extension):
        return f"{result_folder_name}/{file_name}.{extension}"
