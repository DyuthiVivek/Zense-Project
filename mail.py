from email.message import EmailMessage
import ssl
import smtplib
from get_credentials import get_email, get_sender_address, get_sender_password

def send_mail(body, subject):

    # get details from config file
    email_sender = get_sender_address()
    email_password = get_sender_password()
    email_receiver = get_email()
    
    # compose mail
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    # sending the mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    
    print('mail sent!')