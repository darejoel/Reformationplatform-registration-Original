import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


sender_password= "fbou eflm dczd xokb"
server_email= "joedre2000@gmail.com"
subject= "RP CODE"
body= 'just checking on you '
reciever_email= 'mythicmotionsmedia@gmail.com'
ministry= "admin@reformationplatform.com"

# Email content
msg = MIMEMultipart()
msg['Subject'] = subject
msg['From'] = server_email
msg['To'] = reciever_email

msg.attach(MIMEText(body, 'plain'))

# Send email
try:
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(server_email, sender_password)
        text= msg.as_string()
        smtp.sendmail(server_email, reciever_email, text)
        print("Email sent successfully!")

except Exception as e:
    print(f"Error: unable to send mail\n{e}")






