import smtplib
import os 
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get('ignaciotomas.t@gmail.com')
EMAIL_PASS = os.environ.get('mecano311998+')

msg = EmailMessage()
msg['subject'] = "TEST"
msg['from'] = 'plain'
msg['to'] = 'ignaciotomas.t@gmail.com'
msg.set_content("Hola esto es una prueba")

with smtplib.SMTP_SSL('smtp.gmail.com',334) as smtp:
    smtp.login(EMAIL_ADDRESS,EMAIL_PASS)
    smtp.send_message(msg)