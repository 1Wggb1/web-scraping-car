import smtplib,  ssl
from email.message import EmailMessage
import os
from typing import Final


class MailSender:
    FROM: Final = os.environ["EMAIL"]
    FROM_ID: Final = os.environ["EMAIL_ID"]
    TO: Final = os.environ["TO_EMAIL"]

    def send(self, provider_name, content):
        msg = EmailMessage()
        msg["Subject"] = f"New ad´s found on {provider_name}"
        msg["From"] = MailSender.FROM
        msg["To"] = MailSender.TO
        msg.set_content(content)

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp_server:
            smtp_server.starttls()
            smtp_server.login(MailSender.FROM, MailSender.FROM_ID)
            smtp_server.send_message(msg)