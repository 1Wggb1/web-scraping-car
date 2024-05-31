from src.result.file_result import FileResult
from src.scraping.icarros_scraping import ICarrosScraping

if __name__ == "__main__":
    file_result = FileResult()
    icarros_scraping = ICarrosScraping(
        "?ord=35&&sop=esc_2.1_-cid_9668.1_-rai_50.1_-prf_44000.1_-kmm_100000.1_-mar_14.1_-mod_1052.1_-cam_false.1_-ami_2011.1_-",
         file_result)
    icarros_scraping.start_car_scraping()