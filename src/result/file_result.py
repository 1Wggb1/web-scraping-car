class FileResult:

    def write(self, file_name: str, content: str):
        with open(f"../results/{file_name}", "a", encoding="utf-8") as file:
            print("Writing file result")
            file.write(content)