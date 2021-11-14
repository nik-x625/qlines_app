import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logger_custom import get_module_logger

default_address = 'mabolfathi@gmail.com'

fromaddr = "wpmessages1050@gmail.com"
password = 'gj46_d3tgn14nvlsw'

logger = get_module_logger(__name__)


def send_email(message_dict, toaddr=None):
    if not toaddr:
        toaddr = default_address

    logger.debug('picked from queue, in send_email method')

    msg = MIMEMultipart()
    msg['From'] = "Q-Lines Contact Page"
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
    '''.format("Q-Lines contact form",
               message_dict['subject'],
               message_dict['first_name'],
               message_dict['last_name'],
               message_dict['email'],
               message_dict['datetime'],
               message_dict['message']
               )

    logger.debug(
        'picked from queue, in send_email method, going to login to gmail and submit the email')

    # 'message_dict['message'], 'plain'))
    msg.attach(MIMEText(message_html, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    logger.debug(
        'picked from queue, in send_email method, the login result is: '+str(text))
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    logger.debug(
        'picked from queue, in send_email method, the email sending attempt done')

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









def send_email_async(msg, toaddr=None):
    '''
    This method is called by RQ Worker
    '''

    if not toaddr:
        toaddr = default_address

    logger.debug('# in async email func, start....')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    logger.debug('# fromaddr: '+str(fromaddr))
    logger.debug('# toaddr: '+str(toaddr))
    logger.debug('# text: '+str(text))

    logger.debug('# in async email func, end....')

    return True


def send_email_contact(message_dict):
    '''
    This method is called by Flask route of '/contact'
    '''

    msg = MIMEMultipart()
    msg['From'] = "FLUENCE24"
    msg['To'] = default_address
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
    '''.format("FLUENCE24 contact form",
               message_dict.get('subject', ''),
               message_dict.get('first_name', ''),
               message_dict.get('last_name', ''),
               message_dict.get('email', ''),
               message_dict.get('datetime', ''),
               message_dict.get('message', '')
               )

    logger.debug('# contact contents to send as email: '+str(message_html))

    msg.attach(MIMEText(message_html, 'plain'))

    try:
        email_result = q.enqueue(send_email_async, msg)
        # logger.debug('# enqueueing result: '+str(email_result))
    except Exception as e:
        logger.debug('# email enqueue error: '+str(e))
        return False

    return "The message sent successfully!"

def send_email_signup(toaddr):
    '''
    This method is called by Flask route of '/signup'
    '''

    if not toaddr:
        toaddr = default_address

    msg = MIMEMultipart()
    msg['From'] = "Fluence24"
    msg['To'] = toaddr
    msg['Subject'] = "Confirm your email address!"

    logger.debug('# send_email_signup, sending to: '+str(toaddr))
    logger.debug('# send_email_signup, msg: '+str(msg))

    """
    message_html = '''
    Submitted in portal: {}
    Subject: {}
    First name: {}
    Last name: {}
    Email address: {}
    Date/Time: {}

    Message:
    {}
    '''.format("FLUENCE24 contact form",
               message_dict.get('subject', ''),
               message_dict.get('first_name', ''),
               message_dict.get('last_name', ''),
               message_dict.get('email', ''),
               message_dict.get('datetime', ''),
               message_dict.get('message', '')
               )
    """

    msg.attach(MIMEText("Confirm your email address!", 'plain'))

    try:
        email_result = q.enqueue(send_email_async, msg, toaddr)
    except Exception as e:
        logger.debug('# in send_email_signup, email enqueue error: '+str(e))
        return False

    logger.debug('# in send_email_signup, send_email result: ' +
                 str(email_result))
    return True





if __name__ == "__main__":
    send_email({'first_name': '', 'last_name': '', 'email': '',
                'subject': '', 'message': 'xx', 'datetime': 'fff'})
