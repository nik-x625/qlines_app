#!/usr/bin/python
from rq import Queue
import redis
import os
import requests

import clickhouse_connect

from datetime import datetime as dt

from flask import (Flask, Response, abort, current_app, json, jsonify,
                   make_response, redirect, render_template, request, session,
                   url_for)

from flask_login import (LoginManager, UserMixin, login_required, login_user,
                         logout_user, LoginManager)

from email_module import *
from flask_pager import Pager
from mongodb_module import *

from logger_custom import get_module_logger

logger = get_module_logger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(42)
app.config['PAGE_SIZE'] = 10
app.config['VISIBLE_PAGE_COUNT'] = 5

# initialise the flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# for long running functions
r = redis.Redis()
q = Queue('app1', connection=r)


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# create some users with ids 1 to 5
users = [User(id) for id in range(1, 5)]


@app.route('/', methods=['GET', 'POST'])
def index():
    logger.debug('in flask, route is /')
    return render_template('index.html')


# highcharts test page, from: https://github.com/soumilshah1995/Stockchart-highchart-flask-
@app.route('/test', methods=['GET', 'POST'])
def index_test():
    logger.debug('in flask, route is /test')
    return render_template('test_mychart.html')

# to fetch data from jquery, highcharts


def sortFn(tpl):
    return tpl[1]


@app.route('/fetchdata', methods=["GET", "POST"])
def fetchdata():
    # logger.debug('# the fetching data api called')

    client_name = request.args.get('client_name', None)
    param_name = request.args.get('param_name', None)
    table_name = request.args.get('table_name', None)
    single_data = request.args.get('single_data', None)

    #ts_start = request.args.get('ts_start', None)
    #ts_end = request.args.get('ts_end', None)
    limit = 200

    client = clickhouse_connect.get_client(
        host='localhost', port='7010', username='default')

    result = client.query("SELECT param_name, ts, param_value FROM {} WHERE client_name='{}' and param_name='{}' ORDER BY ts DESC LIMIT {}".format(
        table_name, client_name, param_name, limit))

    data = result.result_set

    data.sort(key=sortFn)

    if single_data:
        limit = 1
        result = client.query("SELECT param_name, ts, param_value FROM {} WHERE client_name='{}' and param_name='{}' ORDER BY ts DESC LIMIT {}".format(
            table_name, client_name, param_name, limit))
        data = result.result_set
        #data=[('pp','Sat, 19 Nov 2022 17:19:06 GMT',120)]

    logger.debug('# data to revert to FE is: '+str(data[0][2]))
    return {'name': 'some name here', 'data': data}


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    logger.debug('in flask, route is /login')

    logger.debug('')
    logger.debug('# request.form: ' + str(request.form))
    logger.debug('# request.args: ' + str(request.args))
    logger.debug('# request.args.get("next"): ' +
                 str(request.args.get("next")))

    if request.method == 'POST':
        email = request.form.get('email_holder', None)
        password = request.form.get('password_holder', None)
        keepsignedin = request.form.get('keepsignedin_holder', None)

        # To remember the user even if browser is closed
        if keepsignedin == "on":
            remember_me_flag = True
        else:
            remember_me_flag = False

        login_success = 0

        user_doc = read_user_doc(email)
        if not user_doc:
            return render_template('login.html', login_message='The username does not exist!')

        if user_doc.get('password', None) == password:
            login_success = 1

        if login_success:
            next = request.args.get('next')
            login_user(User(2), remember=remember_me_flag)
            return redirect(next or url_for('dashboard'))
        else:
            return render_template('login.html', login_message='The password is not correct!')

    else:

        return render_template('login.html', login_message="Sign in to continue...")


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    logger.debug('in flask, route is /signup, method: ' + str(request.method))

    logger.debug('')
    logger.debug('# in signup, request.form: ' + str(request.form))
    logger.debug('# in signup, request.args: ' + str(request.args))
    logger.debug('# in signup, request.args.get("next"): ' +
                 str(request.args.get("next")))

    if request.method == 'POST':
        logger.debug('# post method arrived, going to update mongo')

        email = request.form.get('email', None)
        agreeterms = request.form.get('agreeterms', None)

        password_main = request.form.get('password_main', None)
        password_confirm = request.form.get('password_confirm', None)
        if password_main != password_confirm:
            return render_template('signup.html', message='Passwords do not match!')

        if not agreeterms:
            return render_template('signup.html', message='Please read the terms and conditions.')

        country = request.form.get('country', None)
        new_user_data = {
            'email': email,
            'password': password_main,
            'agreeterms': agreeterms,
            'time-formatted': dt.now().strftime("%Y-%m-%d %H:%M:%S"),
            'time': dt.now()
        }

        message_dict = {'email': email,
                        'confirmation_link': 'https://www.qlines.net/confirmation/wertgwekjnekrg'}

        create_user_result = create_new_user(new_user_data)

        if create_user_result:
            return render_template('confirm_registration.html')
        else:
            return render_template('signup.html', message='The user already exists!')

        # todo: enable email confirmation for sign up requests, for the moment, for MVP it is not necessary,
        # send_email_signup(message_dict)

    else:
        return render_template('signup.html', message='Signing up is easy. It only takes a few steps')


# somewhere to logout
@app.route("/logout")
def logout():
    logger.debug('in flask, route is /logout')
    logout_user()
    return render_template('index.html')


@app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
def dashboard():
    logger.debug('in flask, route is /dashboard')
    # return render_template('dashboard.html')
    return render_template('dashboard.html')


@app.route('/products', methods=['GET', 'POST'])
def products():
    logger.debug('in flask, route is /products')
    return render_template('index.html')


@app.route('/pricing', methods=['GET', 'POST'])
def pricing():
    logger.debug('in flask, route is /pricing')
    return render_template('pricing.html')


# Used to show the contact page and also POST method to submit the message
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    result = ''
    logger.debug('in flask, in the contact function')
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
            'datetime': dt.now().strftime("%Y-%m-%d %H:%M:%S")}

        email_result = q.enqueue(send_email_contact, message_dict)
        logger.debug('# email_result: ' + str(email_result))

        if email_result:
            result = 'Your message sent successfully. Thank you!'

    return render_template('contact.html', result=result)

#
#
#
#
#
#

# handle login failed


@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)

#
#
#
#
#
#


@app.route('/search_backend', methods=['GET', 'POST'])
def search_backend():
    logger.debug('in flask, route is /search_backend')

    results = []  # sample_insta_data_maker()

    page = request.form.get('page', 1)

    if not page.isdigit():
        page = 1
    page = int(page)

    count = len(results)
    pager = Pager(page, count)
    pages = pager.get_pages()

    skip = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = results[skip:skip + limit]

    return render_template('search_result.html',
                           results=data_to_show,
                           pages=pages)

#
#
#
#
#
# By ML - for testing if he can do this


@app.route('/sms-panel', methods=['GET', 'POST'])
@login_required
def smspanel():
    return render_template('ml_sms-panel.html')


@app.route('/mashin-panel', methods=['GET', 'POST'])
@login_required
def mashinpanel():
    return render_template('ml_mashin-panel.html')


@app.route('/call-panel', methods=['GET', 'POST'])
@login_required
def callpanel():
    return render_template('ml_call-panel.html')


@app.route('/more', methods=['GET', 'POST'])
@login_required
def more_func():
    return render_template('ml_more.html')


# test only
users = {'foo@bar.tld': {'password': 'secret'}}
#
#
#
#
#
#


if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=8080, debug=True)
