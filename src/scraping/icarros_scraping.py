import datetime
from src.result.file_result import FileResult
from src.scraping.scraping import Scraping
from src.util.logger import log


def create_file_name():
    scraping_datetime = datetime.datetime.now().strftime("%d_%m_%Y-%H_%M")
    return f"icarros_search-{scraping_datetime}.html"


#Example of filter_query_param 
# "?ord=35&&sop=esc_2.1_-cid_9668.1_-rai_50.1_-prf_44000.1_-kmm_100000.1_-mar_14.1_-mod_1052.1_-cam_false.1_-ami_2011.1_-"
def assembly_site_url(filter_query_param, page_number):
    return f"{ICarrosScraping.SITE_URL}?pag={page_number}&{filter_query_param}"


class ICarrosScraping(Scraping):
    SITE_URL = "https://www.icarros.com.br/ache/listaanuncios.jsp"
    CAR_CARD_HTML_ELEMENT = "ul"
    CAR_CARD_CSS_ID = "cards-grid"
    CAR_RESULT_TITLE_HTML_ELEMENT = "span"
    CAR_RESULT_TITLE_CSS_CLASS = "title__onLight ids_textStyle_overline header-list__subtitle header-list__subtitle--block"
    CAR_PROGRESS_BAR_ELEMENT = "progress"
    CAR_PROGRESS_BAR_CSS_CLASS = "pagination__progress-bar"

    def __init__(self, search_filter_params, file_result: FileResult):
        self.search_filter_params = search_filter_params
        self.file_result = file_result

    def start_car_scraping(self):
        log.info("Starting icarros scraping...")
        results = self.do_cars_scraping()
        if len(results) == 0:
            log.warn("No result found on icarros scraping ⊙﹏⊙∥")
            return

        log.info("Writing icarros scraping result...")
        self.write_results(create_file_name(), results)

    def do_cars_scraping(self):
        results = []
        first_page_search = self.search(assembly_site_url(self.search_filter_params, 1))

        title = self.get_title(first_page_search)
        results.insert(0, title)
        car_cards = self.get_car_cards(first_page_search)

        results.append(car_cards)
        ads_data = self.extract_ads_data(car_cards)

        max_page = self.get_max_page(first_page_search)
        for page in range(2, max_page + 1):
            car_cards = self.get_car_cards(self.do_car_scraping(page))
            ads_data |= self.extract_ads_data(car_cards)
            results.append(car_cards)

        strftime = datetime.datetime.now().strftime("%d_%m_%Y-%H_%M")
        self.file_result.write(f"ad_data-{strftime}.json", ads_data.__str__())

        #results.extend([self.get_car_cards(self.do_car_scraping(page)) for page in range(2, max_page + 1)])
        return results

    def extract_ads_data(self, car_cards):
        result = {}
        imgs = car_cards.findAll("img")
        for img in imgs:
            val = self.extract_onclick_value(img)
            key = self.extract_ad_idx_position(val)
            result[key] = val
        return result

    def extract_onclick_value(self, element):
        onclick_val = element.attrs["onclick"]
        onclick_val = onclick_val[onclick_val.index("(") + 1:]
        return onclick_val[:len(onclick_val) - 1]

    def extract_ad_idx_position(self, onclick_val):
        idx_start_position = onclick_val.find("index: ")
        ad_idx_start_position = idx_start_position + 7
        ad_idx_final_position = onclick_val[ad_idx_start_position:].find(",")
        return int(onclick_val[ad_idx_start_position:ad_idx_start_position + ad_idx_final_position])

    def do_car_scraping(self, page_number):
        return self.search(assembly_site_url(page_number))

    def get_title(self, scraping_result):
        return self.filter(scraping_result,
                           ICarrosScraping.CAR_RESULT_TITLE_HTML_ELEMENT,
                           {"class": ICarrosScraping.CAR_RESULT_TITLE_CSS_CLASS})

    def get_car_cards(self, scraping_result):
        return self.filter(scraping_result,
                           ICarrosScraping.CAR_CARD_HTML_ELEMENT,
                           {"id": ICarrosScraping.CAR_CARD_CSS_ID})

    def get_max_page(self, scraping_result):
        filtered_item = self.filter(scraping_result,
                                    ICarrosScraping.CAR_PROGRESS_BAR_ELEMENT,
                                    {"class": ICarrosScraping.CAR_PROGRESS_BAR_CSS_CLASS})
        return int(filtered_item.attrs["max"])

    def write_results(self, file_name, results):
        for result in results:
            self.file_result.write(file_name, result.prettify())
