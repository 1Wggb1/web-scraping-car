from src.result.file_result_repository import FileResultRepository
from src.scraping.scraping import Scraping
from src.result.file_result import FileResult
import json
from src.util.logger_util import log


def parse_results_to_json(results):
    return json.loads(results)


def assembly_site_url(car_model_path, encoded_query_param):
    return f"{WebmotorsScraping.SITE_URL}{car_model_path}{encoded_query_param}"


class WebmotorsScraping(Scraping, FileResult):
    SITE_URL = "https://www.webmotors.com.br/api/search/car?url=https://www.webmotors.com.br/carros"
    RESULT_FILE_EXTENSION = "json"
    REPOSITORY_FILE_NAME = "/webmotors/found_results.json"

    def __init__(self, car_model_path, encoded_query_params):
        self.car_model_path = car_model_path
        self.encoded_query_params = encoded_query_params
        self.repository = FileResultRepository(WebmotorsScraping.REPOSITORY_FILE_NAME, self)

    def start_car_scraping(self):
        log.info("Starting webmotors scraping...")
        results = self.do_car_search()
        if not len(results):
            log.info("No result found on webmotors scraping ⊙﹏⊙∥")
            return
        log.info("Webmotors scraping result...")
        self.do_car_scarping(results)

    def do_car_scarping(self, results):
        found_results = parse_results_to_json(results)
        search_results = found_results["SearchResults"]
        ad_data = {}
        for result in search_results:
            del result["Media"]
            key = str(result["UniqueId"])
            ad_data[key] = result
        self.repository.merge(ad_data)

    def do_car_search(self):
        return self.search(assembly_site_url(self.car_model_path, self.encoded_query_params))

