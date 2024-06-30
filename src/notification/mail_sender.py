import json
import smtplib
from email.message import EmailMessage
import os
from typing import Final
from src.util.map_util import get_key_or_default
from src.util.logger_util import log


class MailSender:
    FROM: Final = os.environ["EMAIL"]
    FROM_ID: Final = os.environ["EMAIL_ID"]
    PREFERENCES: Final = os.environ["PREFERENCES"]

    def send(self, provider_name, content, car_model):
        preferences = json.loads(json.dumps(MailSender.PREFERENCES))
        log.info(f"{preferences}")
        model_preferences = get_key_or_default(preferences, car_model.lower())
        if not model_preferences:
            log.warn("Model preferences not found")
            return
        recipients = get_key_or_default(model_preferences, "recipients")
        if not recipients:
            log.warn("Model recipients not found")
            return

        msg = EmailMessage()
        msg["Subject"] = f"New ad´s found of {car_model} on {provider_name}"
        msg["From"] = MailSender.FROM
        msg["To"] = recipients
        msg.set_content(content)

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp_server:
            smtp_server.starttls()
            smtp_server.login(MailSender.FROM, MailSender.FROM_ID)
            smtp_server.send_message(msg)