from src.notification.mail_sender import MailSender
from src.result.file_result_repository import FileResultRepository
from src.scraping.scraping import Scraping
from src.result.file_result import FileResult
import json
from src.util.logger_util import log
from typing import Final
from src.util.map_util import get_key_or_default


class WebmotorsScraping(Scraping, FileResult):
    MAIN_URL: Final = "https://www.webmotors.com.br"
    SITE_URL: Final = f"https://www.webmotors.com.br/api/search/car?url={MAIN_URL}/carros"
    RESULT_FILE_EXTENSION: Final = "json"
    REPOSITORY_FILE_NAME: Final = "/webmotors/found_results.json"
    MAPS_ZIPCODE_URL: Final = "https://www.google.com/maps/search"
    RESULTS_PER_PAGE: Final = 35

    def __init__(self, car_model, car_model_path, encoded_query_params):
        self.car_model = car_model
        self.car_model_path = car_model_path
        self.encoded_query_params = encoded_query_params
        self.repository = FileResultRepository(WebmotorsScraping.REPOSITORY_FILE_NAME, self)
        self.mail_sender = MailSender()

    def get_latest_cars(self):
        return self.repository.find_latest()

    def start_car_scraping(self):
        log.info("Starting webmotors scraping...")
        results = self.do_car_search()
        if not len(results):
            log.info("No result found on webmotors scraping ⊙﹏⊙∥")
            return
        log.info("Webmotors scraping result...")
        self.do_car_scarping(results)

    def do_car_scarping(self, results):
        found_results = WebmotorsScraping.__parse_results_to_json(results)
        search_results = found_results["SearchResults"]
        ad_data = {}
        ad_data[self.car_model] = {}

        ad_of_model = ad_data[self.car_model]
        self.add_ads_result(search_results, ad_of_model)
        max_pages = WebmotorsScraping.calculate_max_pages(found_results["Count"])
        self.do_scraping_on_pages(2, max_pages, ad_of_model)

        new_content: dict = self.repository.diff_from_persistent(ad_of_model, self.car_model)
        self.repository.merge(ad_of_model, self.car_model)
        self.__notify(new_content)

    @staticmethod
    def calculate_max_pages(results_size):
        return (results_size // WebmotorsScraping.RESULTS_PER_PAGE) + 1

    def add_ads_result(self, search_results, ad_data):
        for result in search_results:
            if result.get("Media"):
                del result["Media"]
            result_id = str(result["UniqueId"])
            car_result = self.create_result(WebmotorsScraping.__assembly_ad_url(result, result_id), result)
            ad_data[result_id] = car_result

    def do_scraping_on_pages(self, start_page: int, max_page: int, ads_data: dict):
        for page in range(start_page, max_page + 1):
            results = self.do_car_search(page)
            found_results = WebmotorsScraping.__parse_results_to_json(results)
            search_results = found_results["SearchResults"]
            self.add_ads_result(search_results, ads_data)

    def __notify(self, new_content):
        if new_content:
            log.info("Webmotors sending notification")
            self.__do_notify(WebmotorsScraping.__create_notify_object(new_content))

    @staticmethod
    def __create_notify_object(ad_data):
        response = {}
        for key in ad_data:
            ad = ad_data.get(key)
            car = get_key_or_default(ad, "car")
            car_spec = get_key_or_default(car, "Specification")
            car_seller = get_key_or_default(car, "Seller")
            ad_url = get_key_or_default(ad, "ad_url")
            response[ad_url] = {
                "model": get_key_or_default(car_spec, "Title"),
                "color": WebmotorsScraping.__color(car_spec),
                "city": get_key_or_default(car_seller, "City"),
                "mapsLocation": WebmotorsScraping.__create_maps_url(car_seller),
                "year": get_key_or_default(car_spec, "YearFabrication"),
                "km": get_key_or_default(car_spec, "Odometer"),
                "price": WebmotorsScraping.__get_price(car),
            }
        return json.dumps(response, indent=4)

    @staticmethod
    def __color(car_spec):
        color = get_key_or_default(car_spec, "Color")
        return get_key_or_default(color, "Primary")

    @staticmethod
    def __create_maps_url(car_seller_map):
        localization = get_key_or_default(car_seller_map, "Localization")
        if not isinstance(localization, list):
            return ""
        if localization:
            zip_code = get_key_or_default(localization[0], "ZipCode")
            return f"{WebmotorsScraping.MAPS_ZIPCODE_URL}/{zip_code}"

    @staticmethod
    def __get_price(car_map):
        prices = get_key_or_default(car_map, "Prices")
        return get_key_or_default(prices, "Price")

    def __do_notify(self, content):
        self.mail_sender.send("webmotors", content, self.car_model)

    @staticmethod
    def __assembly_ad_url(result, result_id):
        slash_separator = "/"
        specification = get_key_or_default(result, "Specification")
        return (WebmotorsScraping.MAIN_URL + slash_separator
                + "comprar" + slash_separator
                + WebmotorsScraping.__assembly_car_basic_info(specification, "Make") + slash_separator
                + WebmotorsScraping.__assembly_car_basic_info(specification, "Model") + slash_separator
                + WebmotorsScraping.__assembly_car_version(specification) + slash_separator
                + WebmotorsScraping.__assembly_car_ports(specification) + slash_separator
                + WebmotorsScraping.__assembly_car_fabrication_model(specification) + slash_separator
                + result_id).lower()

    @staticmethod
    def __assembly_car_basic_info(specification, field):
        field_object = get_key_or_default(specification, field)
        return get_key_or_default(field_object, "Value")

    @staticmethod
    def __assembly_car_version(specification):
        version = WebmotorsScraping.__assembly_car_basic_info(specification, "Version")
        return (version
                .replace(" ", "-")
                .replace(".", ""))

    @staticmethod
    def __assembly_car_ports(specification):
        return get_key_or_default(specification, "NumberPorts") + "-portas"

    @staticmethod
    def __assembly_car_fabrication_model(specification):
        fabrication_year = get_key_or_default(specification, "YearFabrication")
        model_year = get_key_or_default(specification, "YearModel")
        model_year_parsed = int(model_year) if isinstance(model_year, float) else model_year
        return fabrication_year + "-" + str(model_year_parsed)

    @staticmethod
    def __parse_results_to_json(results):
        return json.loads(results)

    @staticmethod
    def __assembly_site_url(car_model_path, encoded_query_param):
        return f"{WebmotorsScraping.SITE_URL}{car_model_path}{encoded_query_param}"

    def do_car_search(self, page_number=1):
        return self.search(WebmotorsScraping.__assembly_site_url(
            self.car_model_path,
            self.encoded_query_params + f"&actualPage={page_number}&displayPerPage={WebmotorsScraping.RESULTS_PER_PAGE}"))
