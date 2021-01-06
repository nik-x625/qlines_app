#!/usr/bin/python
from rq import Queue
import redis
import logging
import logging.config
import time
import os

from flask import *
from flask import Flask, session, json, jsonify, request, make_response, current_app, abort, render_template
from flask import redirect
from flask_pager import Pager

from mongodb_module import *
from datetime import datetime
from email_module import *

app = Flask(__name__)
app.secret_key = os.urandom(42)
app.config['PAGE_SIZE'] = 10
app.config['VISIBLE_PAGE_COUNT'] = 5


logging.config.fileConfig(fname='logging_config.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger(__name__)


# for long running jobs
r = redis.Redis()
q = Queue('insta', connection=r)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/search_backend', methods=['GET', 'POST'])
def search_backend():

    image_list = ['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgfO1Mq0Kcpp5TjqGOja-AnEFkpFLAav4R0g&usqp=CAU',
                  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBwgu1A5zgPSvfE83nurkuzNEoXs9DMNr8Ww&usqp=CAU',
                  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGqeiMvcMA8ATx6McIgv0QgGq9njL6_9Q9Ww&usqp=CAU',
                  ]

    results = [
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 14, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 29, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 32, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 43, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 55, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 67, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 32, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 43, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 55, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 67, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname3', 'id': 'testid3', 'avglikesppost': 79, 'postspw': 5,
            'followers': '1593476', 'following': 193,   'img': image_list[2]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 43, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 55, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 67, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname3', 'id': 'testid3', 'avglikesppost': 79, 'postspw': 5,
            'followers': '1593476', 'following': 193,   'img': image_list[2]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 32, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 43, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 55, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 67, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname3', 'id': 'testid3', 'avglikesppost': 79, 'postspw': 5,
            'followers': '1593476', 'following': 193,   'img': image_list[2]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 55, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 67, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 32, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 43, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 55, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 67, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname3', 'id': 'testid3', 'avglikesppost': 79, 'postspw': 5,
            'followers': '1593476', 'following': 193,   'img': image_list[2]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 43, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 55, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 67, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname3', 'id': 'testid3', 'avglikesppost': 79, 'postspw': 5,
            'followers': '1593476', 'following': 193,   'img': image_list[2]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 32, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 43, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 55, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 67, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname3', 'id': 'testid3', 'avglikesppost': 79, 'postspw': 5,
            'followers': '1593476', 'following': 193,   'img': image_list[2]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 55, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 67, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 32, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 43, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 55, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 67, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname3', 'id': 'testid3', 'avglikesppost': 79, 'postspw': 5,
            'followers': '1593476', 'following': 193,   'img': image_list[2]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 43, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 55, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 67, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname3', 'id': 'testid3', 'avglikesppost': 79, 'postspw': 5,
            'followers': '1593476', 'following': 193,   'img': image_list[2]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 32, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 43, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname1', 'id': 'testid1', 'avglikesppost': 55, 'postspw': 12,
            'followers': '42345', 'following': 112, 'img': image_list[0]},
        {'name': 'testname2', 'id': 'testid2', 'avglikesppost': 67, 'postspw': 32,
            'followers': '86', 'following': 242,        'img': image_list[1]},
        {'name': 'testname3', 'id': 'testid3', 'avglikesppost': 79, 'postspw': 5,
            'followers': '1593476', 'following': 193,   'img': image_list[2]},
    ]

    page = request.form.get('page', 1)

    if not page.isdigit():
        page = 1
    page = int(page)

    count = len(results)
    pager = Pager(page, count)
    pages = pager.get_pages()

    skip = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = results[skip: skip + limit]

    return render_template('search_result.html', results=data_to_show, pages=pages)


# Used to show the contact page and also POST method to submit the message
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    result = ''
    logger.debug('in contact function 1')
    if request.method == 'POST':

        fname = request.form['fname']
        lname = request.form['lname']
        subject = request.form['subject']
        email = request.form['email']
        message = request.form['message']

        message_dict = {
            'first_name': fname,
            'last_name': lname,
            'email': email,
            'subject': subject,
            'message': message,
            'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        email_result = None
        try:
            email_result = q.enqueue(send_email, message_dict)
        except Exception as e:
            # logger.debug('# email enqueue error: '+str(e))
            print('# email enqueue error: '+str(e))

        print('# email_result - voip: ' + str(email_result))

        if email_result:
            result = 'Your message sent successfully. Thank you!'

    return render_template('contact.html', result=result)







# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/x')
def indexx():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/loginx', methods=['GET', 'POST'])
def loginx():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logoutx')
def logoutx():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
















if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=8080, debug=True)
