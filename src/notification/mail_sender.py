import smtplib
from email.message import EmailMessage
import os
from typing import Final


class MailSender:
    FROM: Final = os.environ["EMAIL"]
    FROM_ID: Final = os.environ["EMAIL_ID"]

    def send(self, provider_name, content, car_model, recipients):

        print(provider_name, content, car_model, recipients)
        msg = EmailMessage()
        msg["Subject"] = f"New ad´s found of {car_model} on {provider_name}"
        msg["From"] = MailSender.FROM
        msg["To"] = recipients
        msg.set_content(content)

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp_server:
            smtp_server.starttls()
            smtp_server.login(MailSender.FROM, MailSender.FROM_ID)
            smtp_server.send_message(msg)