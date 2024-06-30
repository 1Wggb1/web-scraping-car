from src.scraping.icarros_scraping import ICarrosScraping
#from src.scraping.olx_scraping import OlxScraping
from src.scraping.webmotors_scraping import WebmotorsScraping

if __name__ == "__main__":
    #search examples
    brand = "Fiat 500"
    icarros_scraping = ICarrosScraping(brand,
        "sop=esc_2.1_-cid_9668.1_-rai_50.1_-prf_44000.1_-kmm_100000.1_-mar_14.1_-mod_1052.1_-cam_false.1_-ami_2011.1_-")
    icarros_scraping.start_car_scraping()

    webmotors_scraping = WebmotorsScraping(brand, 
                                           "/sp/fiat/500/de.2011",
                                           "%2Fsp%2Ffiat%2F500%2Fde.2011%3Festadocidade%3DS%25C3%25A3o%2520Paulo%26tipoveiculo%3Dcarros%26anode%3D2011%26kmate%3D100000%26marca1%3DFIAT%26modelo1%3D500%26precoate%3D44000%26cambio%3DManual%26o%3D5&order=5&showMenu=true&showCount=true&showBreadCrumb=true&testAB=false&returnUrl=false")
    webmotors_scraping.start_car_scraping()

    brand = "Nissan March"
    icarros_scraping = ICarrosScraping(brand,
                                       "sop=esc_2.1_-cid_9668.1_-rai_50.1_-prf_44000.1_-mar_28.1_-mod_2314.1_-kmm_100000.1_-")
    icarros_scraping.start_car_scraping()
    webmotors_scraping = WebmotorsScraping(brand,
                                           "/sp/nissan/march",
                                           "%2Fsp%2Fnissan%2Fmarch%3Festadocidade%3DS%25C3%25A3o%2520Paulo%2520-%2520S%25C3%25A3o%2520Paulo%26tipoveiculo%3Dcarros%26localizacao%3D-23.5666978%2C-46.5874202x50km%26kmate%3D100000%26marca1%3DNISSAN%26modelo1%3DMARCH%26precoate%3D44000&order=1&showMenu=true&showCount=true&showBreadCrumb=true&testAB=false&returnUrl=false&pandora=false")
    webmotors_scraping.start_car_scraping()


    brand = "i30"
    icarros_scraping = ICarrosScraping(brand,
                                       "sop=esc_2.1_-cid_9668.1_-rai_50.1_-prf_40000.1_-kmm_100000.1_-mar_17.1_-mod_1018.1_-cam_false.1_-")
    icarros_scraping.start_car_scraping()
    webmotors_scraping = WebmotorsScraping(brand,
                                           "/sp/hyundai/i30",
                                           "%2Fsp%2Fhyundai%2Fi30%3Festadocidade%3DS%25C3%25A3o%2520Paulo%2520-%2520S%25C3%25A3o%2520Paulo%26tipoveiculo%3Dcarros%26localizacao%3D-23.5666978%2C-46.5874202x50km%26kmate%3D100000%26marca1%3DHYUNDAI%26modelo1%3DI30%26precoate%3D40000%26cambio%3DManual&order=1&showMenu=true&showCount=true&showBreadCrumb=true&testAB=false&returnUrl=false&pandora=false")
    webmotors_scraping.start_car_scraping()

    # olx_scraping = OlxScraping(
    #     "Z0hgFMeCiYT7-Rj5VPuCm/pt-BR/autos-e-pecas/carros-vans-e-utilitarios/fiat/500/estado-sp/sao-paulo-e-regiao.json",
    #     "gb=1&me=100000&pe=44000&sp=1&route=carros-vans-e-utilitarios&route=fiat&route=500&route=estado-sp&route=sao-paulo-e-regiao")
    # olx_scraping.start_car_scraping()
