import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

default_address = 'mabolfathi@gmail.com'

fromaddr = "wpmessages1050@gmail.com"
password = 'spring64'


logger = logging.getLogger(__name__)


def send_email(subject, body, toaddr=None):
    if not toaddr:
        toaddr = default_address

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    logger.debug('sssss')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    return True


if __name__ == "__main__":
    send_email('test_subj2', 'test_body2')
