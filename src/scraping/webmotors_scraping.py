from src.result.file_result_repository import FileResultRepository
from src.scraping.scraping import Scraping
from src.result.file_result import FileResult
import json
from src.util.logger_util import log
from typing import Final


class WebmotorsScraping(Scraping, FileResult):
    MAIN_URL: Final = "https://www.webmotors.com.br"
    SITE_URL: Final = f"https://www.webmotors.com.br/api/search/car?url={MAIN_URL}/carros"
    RESULT_FILE_EXTENSION: Final = "json"
    REPOSITORY_FILE_NAME: Final = "/webmotors/found_results.json"

    def __init__(self, car_model_path, encoded_query_params):
        self.car_model_path = car_model_path
        self.encoded_query_params = encoded_query_params
        self.repository = FileResultRepository(WebmotorsScraping.REPOSITORY_FILE_NAME, self)

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
        for result in search_results:
            if result.get("Media"):
                del result["Media"]
            result_id = str(result["UniqueId"])
            ad_data[result_id] = {
                "ad_url": WebmotorsScraping.__assembly_ad_url(result, result_id),
                "car": result
            }
        self.repository.merge(ad_data)

    @staticmethod
    def __assembly_ad_url(result, result_id):
        slash_separator = "/"
        specification = result["Specification"]
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
        return specification[field]["Value"]

    @staticmethod
    def __assembly_car_version(specification):
        return (specification["Version"]["Value"]
                .replace(" ", "-")
                .replace(".", ""))

    @staticmethod
    def __assembly_car_ports(specification):
        return specification["NumberPorts"] + "-portas"

    @staticmethod
    def __assembly_car_fabrication_model(specification):
        return specification["YearFabrication"] + "-" + str(int(specification["YearModel"]))

    @staticmethod
    def __parse_results_to_json(results):
        return json.loads(results)

    @staticmethod
    def __assembly_site_url(car_model_path, encoded_query_param):
        return f"{WebmotorsScraping.SITE_URL}{car_model_path}{encoded_query_param}"

    def do_car_search(self):
        return self.search(WebmotorsScraping.__assembly_site_url(self.car_model_path, self.encoded_query_params))