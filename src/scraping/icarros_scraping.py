import json
import re

from src.notification.mail_sender import MailSender
from src.result.file_result import FileResult
from src.result.file_result_repository import FileResultRepository
from src.scraping.scraping import Scraping
from src.util.logger_util import log
from typing import Final
from src.util.map_util import get_key_or_default


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
        self.mail_sender = MailSender()
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

    # Example of filter_query_param 
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

        new_content: dict = self.repository.diff_from_persistent(ads_data)
        self.repository.merge(ads_data)
        self.persist_html_result(html_scraping_results)
        self.__notify(new_content)

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
        ads_script = car_cards.select("li script")
        for ad_script in ads_script:
            ad = ICarrosScraping.extract_car_info(ad_script)
            ad_offer = get_key_or_default(ad, "makesOffer")
            ad_url = ICarrosScraping.__get_ad_url(ad_offer)
            ad_id = ICarrosScraping.__get_ad_id(ad_offer)
            result[ad_id] = self.create_result(f"{ICarrosScraping.MAIN_URL}{ad_url}", ad)
        return result

    @staticmethod
    def extract_car_info(ad):
        if not ad or not ad.contents:
            return []
        content = ad.contents
        if not isinstance(content, list) or not content:
            return []
        return json.loads(content[0])

    def get_max_page(self, scraping_result):
        filtered_item = self.filter(scraping_result,
                                    ICarrosScraping.CAR_PROGRESS_BAR_ELEMENT,
                                    {"class": ICarrosScraping.CAR_PROGRESS_BAR_CSS_CLASS})
        return int(filtered_item.attrs["max"])

    def do_scraping_on_pages(self, start_page, max_page: int, ads_data: dict, html_scraping_results: str):
        for page in range(start_page, max_page + 1):
            car_cards = self.get_car_cards(self.do_car_search(page))
            ads_data |= ICarrosScraping.extract_ads_data(car_cards)
            html_scraping_results += car_cards.__str__()

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

    def __notify(self, new_content):
        if new_content:
            log.info("Icarros sending notification")
            self.__do_notify(ICarrosScraping.__create_notify_object(new_content))

    @staticmethod
    def __create_notify_object(new_content):
        response = {}
        for ad_key in new_content:
            ad = new_content.get(ad_key)
            ad_url = get_key_or_default(ad, "ad_url")
            ad_car = get_key_or_default(get_key_or_default(ad, "car"), "makesOffer")
            response[ad_url] = {
                "model": get_key_or_default(ad_car, "name"),
                "color": get_key_or_default(ad_car, "color"),
                "description": get_key_or_default(ad_car, "description"),
                "year": get_key_or_default(ad_car, "productionDate"),
                "km": ICarrosScraping.__get_car_km(ad_car),
                "price": ICarrosScraping.__get_car_price(ad_car),
            }
        return json.dumps(response, indent=4)

    @staticmethod
    def __get_car_km(ad_offer):
        odometer = get_key_or_default(ad_offer, "mileageFromOdometer")
        return get_key_or_default(odometer, "value")

    @staticmethod
    def __get_car_price(ad_offer):
        offer = get_key_or_default(ad_offer, "offers")
        return get_key_or_default(offer, "price")

    def __do_notify(self, content):
        self.mail_sender.send("icarros", content)

    @staticmethod
    def __get_ad_url(ad_offer):
        offer = get_key_or_default(ad_offer, "offers")
        return get_key_or_default(offer, "url")

    @staticmethod
    def __get_ad_id(ad_offer):
        vehicle_identification = get_key_or_default(ad_offer, "vehicleIdentificationNumber")
        identifier_without_letters = re.sub("[^0-9]", "", vehicle_identification)
        return identifier_without_letters