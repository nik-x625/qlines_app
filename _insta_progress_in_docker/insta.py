# Logging
import logging
import logging.config

# Flask
import flask
from flask import Flask, render_template, json, jsonify, request, make_response, current_app, abort

# Mongo
from mongodb_module import *

# Others
import time
from datetime import datetime

from email_module import *

# App initialisation
app = Flask(__name__)
app.secret_key = 'somekey'

# Logger initialisations
logging.config.fileConfig(fname='logging_config.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger(__name__)


# for long running functions
#import redis
#from rq import Queue
#r = redis.Redis()
#q = Queue('saya', connection=r)

@app.route('/', methods=['GET', 'POST'])
def main_clean():
    return render_template('home.html')

@app.route('/index', methods=['GET', 'POST'])
def main_index():
    return render_template('index.html')

@app.route('/index.html', methods=['GET', 'POST'])
def main_index_html():
    return render_template('index.html')


@app.route('/home', methods=['GET', 'POST'])
def main_home():
    return render_template('home.html')

@app.route('/products', methods=['GET', 'POST'])
def products():
    return render_template('products.html')

@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    return render_template('jobs.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('index.html')

# Used to show the contact page and also POST method to submit the message
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    result = ''
    logger.debug('in contact function 1')
    if flask.request.method == 'POST':

        fname = flask.request.form['fname']
        lname = flask.request.form['lname']
        subject = flask.request.form['subject']
        email = flask.request.form['email']
        message = flask.request.form['message']

        message_dict = {
               'first_name': fname,
               'last_name': lname,
               'email': email,
               'subject': subject,
               'message': message,
               'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        email_result = q.enqueue(send_email, message_dict)
        logger.debug('# email_result: ' + str(email_result))

        if email_result:
            result = 'Your message sent successfully. Thank you!'

    return render_template('contact.html', result=result)

# To submit the newsletter
@app.route('/newsletter', methods=['POST'])
def newsletter():
    result = ''
    logger.debug('in newsletter function 1')
    if flask.request.method == 'POST':

        email_address = flask.request.form['email']

        message_dict = {
               'email_address': email_address,
               'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        email_result = q.enqueue(submit_email_for_newsletter, message_dict)
        logger.debug('# in newsletter, email_result: ' + str(email_result))

        if email_result:
            result = 'Your email address is successully submitted. Thank you!'

    return render_template('index.html/#newsletterstatus', result=result)


if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=8080, debug=False)
