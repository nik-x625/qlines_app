#!/usr/bin/python
from rq import Queue
import redis
import os
from datetime import datetime as dt
from email_module import *
from flask_pager import Pager

# MongoDB handlers and methods
from mongodb_module import *

#from clickhouse_module import *

from logger_custom import get_module_logger

from flask_login import (LoginManager, UserMixin, login_required, login_user,
                         logout_user, LoginManager, current_user)
from flask import (Flask, Response, abort, current_app, json, jsonify,
                   make_response, redirect, render_template, request, session,
                   url_for)


logger = get_module_logger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(42)
app.config['PAGE_SIZE'] = 10
app.config['VISIBLE_PAGE_COUNT'] = 5


# initialise the flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# not sure what are these
# users = {'foo@bar.tld': {'password': 'secret'}}
# create some users with ids 1 to 5
# users = [User(id) for id in range(1, 5)]


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


@login_manager.user_loader
def load_user(userid):
    # logger.debug('# userid is: '+str(userid))
    return User(userid)
# initialise the flask_login


# for long running functions
r = redis.Redis()
q = Queue('app1', connection=r)


@app.route('/', methods=['GET', 'POST'])
def index():
    logger.debug('in flask, route is /')
    return render_template('index.html')


@app.route('/dashboard', methods=['GET', 'POST'])
#@login_required
def dashboard():
    return render_template('dash_comingsoon.html')


# Devices overview table - route
@app.route('/devices', methods=['GET', 'POST'])
#@login_required
def devices():
    return render_template('dash_devices.html')


# Devices overview table - data fetcher
@app.route('/api/data')
#@login_required
def table_data():
    temp_username = 'a@b.c'

    search = request.args.get('search[value]')
    logger.debug('# search is: '+str(search))
    
    res = fetch_device_overview('table1', temp_username, 10)
    res['draw'] = request.args.get('draw', type=int)
    logger.debug('# res is: '+str(res))

    return res


def sortFn(tpl):
    return tpl[1]


@app.route('/fetchdata', methods=["GET", "POST"])
@login_required
def fetchdata():

    # logger.debug('# the fetching data api called')

    client_name = request.args.get('client_name', None)

    limit = 30

    parameter_list = ['param1', 'param2']

    data_to_revert = {}

    # the "current_user.name" identifies the user. This way the data for only this user is reverted back to js code in browser to render.
    for param_name in parameter_list:
        res = fetch_data_per_param(user_name=str(current_user.name), client_name=client_name, param_name=param_name, limit=limit)
        res = res.result_set
        res.sort(key=sortFn)
        data_to_revert[param_name] = res

    return {'name': 'some name here', 'data': data_to_revert}



@app.route('/cli', methods=['GET', 'POST'])
@login_required
def cli():
    return render_template('dash_cli.html')


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('dash_settings.html')


@app.route("/logout")
def logout():
    logout_user()
    return render_template('index.html')




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

        # temporary, change it to 0 later
        login_success = 1 # 0


        # temporary, uncomment this block later
        # user_doc = read_user_doc(email)
        # if not user_doc:
        #     return render_template('login.html', login_message='The username does not exist!')

        # if user_doc.get('password', None) == password:
        #     login_success = 1


        if login_success:
            next = request.args.get('next')
            login_user(User(email), remember=remember_me_flag)
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


@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=80, debug=True)
