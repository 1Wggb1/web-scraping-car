import os
from typing import Final
from telepot import Bot
from src.util.logger_util import log

class TelegramSender:
    CHAT_ID: Final = os.environ["CHAT_ID"]
    BOT_TOKEN: Final = os.environ["BOT_TOKEN"]

    def send(self, provider_name, content, car_model):
        try:
            bot = Bot(BOT_TOKEN)
            bot.sendMessage(CHAT_ID, f"<b>{provider_name.upper()} - CAR ADS FOUND</b>\n\n- MODEL = {car_model}\n\n<code>{content}</code>", parse_mode="HTML")
        except Exception as exception:
            log.error(f"Error when sending telegram message. Error message = {exception.__str__()}")