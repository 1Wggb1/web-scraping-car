import os
from typing import Final
from telepot import Bot
from src.util.logger_util import log

class TelegramSender:
    CHAT_ID: Final = os.environ["CHAT_ID"]
    BOT_TOKEN: Final = os.environ["BOT_TOKEN"]

    def send(self, provider_name, content, car_model):
        try:
            bot = Bot(TelegramSender.BOT_TOKEN)
            bot.sendMessage(TelegramSender.CHAT_ID, self.__create_telegram_message(provider_name, content, car_model), parse_mode="HTML")
        except Exception as exception:
            log.error(f"Error when sending telegram message. Error message = {exception.__str__()}")

    def __create_telegram_message(self, provider_name, content, car_model):
        message_header = f"<b>{provider_name.upper()} - CAR ADS FOUND\n\U0001F698 {car_model.upper()}</b>\n\n"
        message_body = ""
        for url, result in content.items():
            message_body += f"\U0001F697\nlink: {url}\n"
            for car_spec, value in result.items():
                message_body += f"{car_spec}: {value}\n"
            message_body += "\n"
        return message_header + message_body