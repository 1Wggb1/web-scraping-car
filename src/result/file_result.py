from src.util.logger_util import log
from src.util.datetime_format_util import get_formatted_datetime


def create_file_name(result_folder_name, extension):
    scraping_datetime = get_formatted_datetime()
    return f"{result_folder_name}/ad_data-{scraping_datetime}.{extension}"


class FileResult:

    def write(self, file_name: str, content: str):
        self.__do_write(file_name, content, "a")

    def __do_write(self, file_name: str, content: str, write_option: str):
        with open(f"../results/{file_name}", write_option, encoding="utf-8") as file:
            log.info("Writing file result")
            file.write(content)

    def override_write(self, file_name: str, content: str):
        self.__do_write(file_name, content, "w")

    def read(self, file_name):
        with open(f"../results/{file_name}", "r", encoding="utf-8") as file:
            return file.read()
