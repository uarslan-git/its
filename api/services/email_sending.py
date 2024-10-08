import smtplib, ssl
import os
from config import config
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail.errors import ConnectionErrors


#def send_mail(message, receiver_email):
#    #https://realpython.com/python-send-email/
#    if config.email_enabled == False:
#        print(message)
#    else:
#        password = os.environ.get("EMAIL_PWD")
#        port = os.environ.get("EMAIL_PORT") #465 For SSL
#        host = os.environ.get("EMAIL_HOST") 
#        sender = os.environ.get("EMAIL_ADRESS")
#
#        context = ssl.create_default_context()
#        with smtplib.SMTP_SSL(host, port, context=context) as server:
#            server.login(sender, password)
#            server.sendmail(
#                sender, receiver_email, message.as_string()
#            )

async def send_mail(message, receiver_email):

    emailconf = ConnectionConfig(
        MAIL_USERNAME=os.environ.get("EMAIL_USR"),
        MAIL_PASSWORD=os.environ.get("EMAIL_PWD"),
        MAIL_FROM=os.environ.get("EMAIL_SENDER"),
        MAIL_PORT=os.environ.get("EMAIL_PORT"),
        MAIL_SERVER=os.environ.get("EMAIL_HOST"),
        MAIL_FROM_NAME="its",
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        #TEMPLATE_FOLDER='./templates/email'
    )


    if config.email_enabled == False:
        print(message)
    else:
        try:
            message_schema = MessageSchema(
            subject="Test",
            recipients=[receiver_email],
            body="Test Message",
            subtype='plain',
            )
            fm = FastMail(emailconf)
            await fm.send_message(message_schema)
        except Exception as e: 
            print(e)
