from src.util.logger_util import log


class FileResult:
    def override_write(self, file_name: str, content: str):
        FileResult.__do_write(file_name, content, "w")

    @staticmethod
    def __do_write(file_name: str, content: str, write_option: str):
        with open(f"./results/{file_name}", write_option, encoding="utf-8") as file:
            log.info("Writing file result")
            file.write(content)

    def read(self, file_name):
        with open(f"./results/{file_name}", "r", encoding="utf-8") as file:
            return file.read()