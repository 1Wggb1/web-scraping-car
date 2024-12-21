import os
from typing import Final
from telepot import Bot
from src.util.logger_util import log
import json

class TelegramSender:
    CHAT_ID: Final = os.environ["CHAT_ID"]
    BOT_TOKEN: Final = os.environ["BOT_TOKEN"]
    MAX_MESSAGE_SIZE: Final = 4095
    FRONT_CAR_ICON: Final = "\U0001F698"
    CAR_ICON: Final = "\U0001F697"

    def send(self, provider_name, content, car_model):
        try:
            bot = Bot(TelegramSender.BOT_TOKEN)
            messages_results = TelegramSender.__create_telegram_messages(provider_name, content, car_model)
            for partial_message_result in messages_results:
                bot.sendMessage(TelegramSender.CHAT_ID, partial_message_result, parse_mode="HTML")
        except Exception as exception:
            log.error(f"Error when sending telegram message. Error message = {exception.__str__()}")

    def __create_telegram_messages(provider_name, content, car_model):
        try:
            return TelegramSender.__do_create_telegram_messages(provider_name, content, car_model)
        except Error as exception:
            raise Error("Error when creating telegram message")

    def __do_create_telegram_messages(provider_name, content, car_model):
        message_header = f"<b>{provider_name.upper()} - CAR ADS FOUND\n{TelegramSender.FRONT_CAR_ICON} {car_model.upper()}</b>\n\n"
        partial_result_message = message_header
        messages_results = []
        for url, result in json.loads(content).items():
            car_result = f"{TelegramSender.CAR_ICON}\n<b>link</b>: {url}\n"
            for car_spec, value in result.items():
                car_result += f"<b>{car_spec}</b>: {value}\n"
            car_result += "\n"
            if len(partial_result_message + car_result) < TelegramSender.MAX_MESSAGE_SIZE:
                partial_result_message += car_result
                continue
            messages_results.append(partial_result_message)
            partial_result_message = f"<b>CONTINUING RESULTS OF {TelegramSender.FRONT_CAR_ICON} {car_model.upper()}</b>\n\n{car_result}"
        return messages_results
