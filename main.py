import json

from src.scraping.icarros_scraping import ICarrosScraping
from src.scraping.webmotors_scraping import WebmotorsScraping

if __name__ == "__main__":
    #search examples
    icarros_scraping = ICarrosScraping(
         "ord=35&&sop=esc_2.1_-cid_9668.1_-rai_50.1_-prf_44000.1_-kmm_100000.1_-mar_14.1_-mod_1052.1_-cam_false.1_-ami_2011.1_-")
    icarros_scraping.start_car_scraping()

    webmotors_scraping = WebmotorsScraping("/sp/fiat/500/de.2011",
    "%2Fsp%2Ffiat%2F500%2Fde.2011%3Festadocidade%3DS%25C3%25A3o%2520Paulo%26tipoveiculo%3Dcarros%26anode%3D2011%26kmate%3D100000%26marca1%3DFIAT%26modelo1%3D500%26precoate%3D44000%26cambio%3DManual%26o%3D5&actualPage=1&displayPerPage=24&order=5&showMenu=true&showCount=true&showBreadCrumb=true&testAB=false&returnUrl=false")
    webmotors_scraping.start_car_scraping()