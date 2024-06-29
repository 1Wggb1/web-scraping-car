import json

from src.result.file_result import FileResult
from src.util.logger_util import log
from src.util.datetime_format_util import get_formatted_datetime
from src.util.map_util import get_key_or_default, get_key_or_empty


class FileResultRepository:
    INFO_KEY = "info"

    def __init__(self, file_name, file_result: FileResult):
        self.file_name = file_name
        self.file_result = file_result

    def persist_all(self, results: str, result_file: str):
        log.info(f"Persisting... result data on file repository on file = {result_file}")
        self.file_result.override_write(result_file, results)

    def merge(self, ad_of_model: dict, car_model):
        persistent_cars_result: dict = self.__find_result() 
        if not persistent_cars_result or not persistent_cars_result.get(car_model):
            persistent_cars_result[car_model] = {}
        persistent_car_model_result: dict = persistent_cars_result[car_model]
        new_results_keys = ad_of_model.keys() - persistent_car_model_result.keys()
        for new_key in new_results_keys:
            persistent_car_model_result[new_key] = ad_of_model[new_key]

        if len(new_results_keys):
            log.info(f"Merging... result data on file repository on file = {self.file_name}")
            persistent_car_model_result[FileResultRepository.INFO_KEY] = FileResultRepository.__generate_update_infos(
                new_results_keys)
            self.file_result.override_write(self.file_name, json.dumps(persistent_cars_result))

    def diff_from_persistent(self, result_data: dict, car_model) -> dict:
        persistent_result: dict = get_key_or_empty(self.__find_result(), car_model)
        new_results_keys = result_data.keys() - persistent_result.keys()
        return {new_key: result_data[new_key] for new_key in new_results_keys}

    @staticmethod
    def __generate_update_infos(results):
        return {
            "lastUpdateDateTime": get_formatted_datetime(),
            "foundResultsIds": list(results),
            "foundResultsSize": len(results)
        }

    def __find_result(self) -> dict:
        read_result = self.file_result.read(self.file_name)
        return json.loads(read_result) if len(read_result) else {}

    def find_latest(self) -> dict:
        read_result = self.file_result.read(self.file_name)
        result_map = json.loads(read_result) if len(read_result) else {}
        if not result_map:
            return {}
        info_val = result_map[FileResultRepository.INFO_KEY]
        if not info_val:
            return {}
        latest_results_ids = info_val["foundResultsIds"]
        return {
            FileResultRepository.INFO_KEY: info_val,
            "results": [result_map[id] for id in latest_results_ids]
        }
