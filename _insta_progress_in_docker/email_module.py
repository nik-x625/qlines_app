import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

default_address = 'mabolfathi@gmail.com'

fromaddr = "wpmessages1050@gmail.com"
password = 'spring64'

logger = logging.getLogger(__name__)

def send_email(message_dict,toaddr=None):
    if not toaddr:
        toaddr = default_address


    msg = MIMEMultipart()
    msg['From'] = "SayaNetworks contact form"
    msg['To'] = toaddr
    msg['Subject'] = message_dict['subject']

    message_html = '''
    Submitted in portal: {}
    Subject: {}
    First name: {}
    Last name: {}
    Email address: {}
    Date/Time: {}

    Message: 
    {}
    '''.format( "SayaNetworks contact form",
                message_dict['subject'],
                message_dict['first_name'],
                message_dict['last_name'],
                message_dict['email'],
                message_dict['datetime'],
                message_dict['message']
                )

    msg.attach(MIMEText(message_html, 'plain')) #'message_dict['message'], 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    return True

def submit_email_for_newsletter(message_dict):
    msg = MIMEMultipart()
    msg['From'] = "Saya newsletter form"
    msg['To'] = default_address
    msg.attach(MIMEText(str(message_dict), 'plain'))
    msg['Subject'] = 'Request for newsletter'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, default_address, text)
    server.quit()
    return True


if __name__ == "__main__":
    send_email('test_subj2','test_body2')
