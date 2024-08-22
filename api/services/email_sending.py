import smtplib, ssl
import os
from config import config

def send_mail(message, receiver_email):
    #https://realpython.com/python-send-email/
    if config.email_enabled == False:
        print(message)
    else:
        password = os.environ.get("EMAIL_PWD")
        port = 465  # For SSL
        host = os.environ.get("EMAIL_HOST") 
        sender = os.environ.get("EMAIL_ADRESS")

        context = ssl.create_default_context()
        #with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(sender, password)
            server.sendmail(
                sender, receiver_email, message.as_string()
            )