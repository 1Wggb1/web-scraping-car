from src.result.file_result import FileResult
from src.result.file_result_repository import FileResultRepository
from src.scraping.scraping import Scraping
import json
from src.util.logger_util import log
from typing import Final


class OlxScraping(Scraping, FileResult):
    MAIN_URL: Final = "https://www.olx.com.br"
    SITE_URL: Final = f"{MAIN_URL}/_next/data/"
    REPOSITORY_FILE_NAME: Final = "/olx/found_results.json"

    def __init__(self, car_path, filter_query_param):
        self.car_path = car_path
        self.filter_query_param = filter_query_param
        self.repository = FileResultRepository(OlxScraping.REPOSITORY_FILE_NAME, self)

    def get_latest_cars(self):
        return self.repository.find_latest()

    def start_car_scraping(self):
        log.info("Starting olx scraping...")
        results = self.do_car_search()
        if not len(results):
            log.info("No result found on olx scraping ⊙﹏⊙∥")
            return
        log.info("Olx scraping result...")
        self.do_car_scarping(results)

    def do_car_search(self):
        return self.search(OlxScraping.__assembly_site_url(self.car_path, self.filter_query_param))

    @staticmethod
    def __assembly_site_url(car_model_path, query_param):
        return f"{OlxScraping.SITE_URL}/{car_model_path}?{query_param}"

    def do_car_scarping(self, results):
        found_results = OlxScraping.__parse_results_to_json(results)
        search_results = found_results["pageProps"]["ads"]
        ad_data = {}
        for result in search_results:
            if result.get("images"):
                del result["images"]
            if result.get("advertisingId"):
                continue
            result_id = str(result["listId"])
            ad_data[result_id] = self.create_result(result["url"], result)
        self.repository.merge(ad_data)
        
    @staticmethod
    def __parse_results_to_json(results):
        return json.loads(results)
