import json
import os
from typing import Final
from src.util.map_util import get_key_or_default

from src.scraping.icarros_scraping import ICarrosScraping
from src.scraping.webmotors_scraping import WebmotorsScraping

PREFERENCES: Final = """{
  "audi a1":{
      "filters": {
             "webmotors": "/sp/audi/a1?estadocidade=S%C3%A3o%20Paulo&tipoveiculo=carros-usados&marca1=AUDI&modelo1=A1&precoate=60000&actualPage=1&displayPerPage=24&order=1&showMenu=true&showCount=true&showBreadCrumb=true&testAB=false&returnUrl=false&pandora=false&mediaZeroKm=false"
       },
       "notificationRecipients": "abcd@gmail.com, efg@gmail.com"
  }
}"""

if __name__ == "__main__":
    prefs = json.loads(PREFERENCES)
    for key, value in prefs.items():
        notification_recipients = get_key_or_default(value, "notificationRecipients")
        filters = get_key_or_default(value, "filters")
        print(filters)
        if not filters:
            continue

        webmotors_scraping = WebmotorsScraping(key, get_key_or_default(filters, "webmotors"), notification_recipients)
        webmotors_scraping.start_car_scraping()

    #scraping object example
    #'{
    # "car model name": {
    #     "filters": {
    #         "webmotors": "/sp/chevrolet/ealta/de.2011%2Fsp%2Fchevrolet%2Fcelta%2Fde.2011%3Festadocidade%3DS%25C3%25A3o%2520Paulo%26tipoveiculo%3Dcarros%26anode%3D2011%26kmate%3D100000%26marca1%3DFIAT%26modelo1%3D500%26precoate%3D44000%26cambio%3DManual%26o%3D5&order=5&showMenu=true&showCount=true&showBreadCrumb=true&testAB=false&returnUrl=false",
    #         "icarros": "sop=esc_2.1_-cid_9668.1_-rai_50.1_-prf_44000.1_-kmm_100000.1_-mar_14.1_-mod_1052.1_-cam_false.1_-ami_2011.1_-"
    #     },
    #     "notificationRecipients": "abcd@gmail.com, efg@gmail.com"
    # },
    # "car model name 2": {
    #     "filters": {
    #         "webmotors": "/sp/hyundai/ix35%2Fsp%2Fhyundai%2Fix35%3Festadocidade%3DS%25C3%25A3o%2520Paulo%26tipoveiculo%3Dcarros%26kmate%3D120000%26marca1%3DHONDA%26modelo1%3DFIT%26precoate%3D45000&order=1&showMenu=true&showCount=true&showBreadCrumb=true&testAB=false&returnUrl=false&pandora=true",
    #         "icarros": "sop=esc_2.1_-cid_9668.1_-rai_50.1_-cam_false.1_-mar_16.1_-mod_233.1_-kmm_120000.1_-prf_44000.1_-"
    #     },
    #     "notificationRecipients": "abcd@gmail.com, efg@gmail.com"
    # }
    # }'