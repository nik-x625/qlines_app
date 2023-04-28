#!/usr/bin/python
'''
main qlines flask app
'''

from redis_utils import enqueue_long_running_function

import os
from datetime import datetime as dt
import logging

from email_module import *
from flask_pager import Pager

# MongoDB handlers and methods
from mongodb_module import create_new_user, timezone_write, create_new_device, read_user_doc

from clickhouse_module import fetch_data_per_param, fetch_device_overview_clickhouse
from token_creator import build_token
from logger_custom import get_module_logger
from flask_login import (LoginManager, UserMixin, login_required, login_user,
                         logout_user, current_user)
from flask import (Flask, Response, abort, current_app, json, jsonify,
                   make_response, redirect, render_template, request, session,
                   url_for)





logger = get_module_logger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(42)
app.config['PAGE_SIZE'] = 10
app.config['VISIBLE_PAGE_COUNT'] = 5
app.config['TEMPLATES_AUTO_RELOAD'] = True

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

#### temporary - for prod remove this
# and change '#@login_required' to '@login_required' in the routes below
# class User:
#     def __init__(self):
#         self.name = None
# current_user = User()
# current_user.name = 'a@a.a'        
#### temporary - for prod remove this


# route to handle the /update_user route, to get 4 parameters from the user and update it in mongodb
# and then redirect to the dashboard
@app.route('/update_user', methods=['GET', 'POST'])
@login_required
def update_user():
    try:
        missing_params_list = []

        params_to_fetch = ['email', 'name', 'phone', 'tz']

        params_dict = {}
        for param in params_to_fetch:

            param_val = request.form.get(param, 0)

            if not param_val:
                missing_params_list.append(param)

            else:
                params_dict[param] = param_val

        logger.debug('# params_dict: '+str(params_dict))

        if missing_params_list:
            logger.debug('# missing_params_list: '+str(missing_params_list))
            return render_template('dash_devices.html', current_username=current_user.name, missing_params_list=missing_params_list)

        else:
            logger.debug('# going to update the user: '+str(params_dict))
            create_new_user(params_dict)
            return redirect(url_for('device_dashx'))

    except Exception as e:
        logger.debug('# in update_user, exception: '+str(e))
        return render_template('dash_devices.html', current_username=current_user.name)
    
def test_update_user():
    params_dict = {}
    params_dict['email'] = 'aa@bb.cc'
    params_dict['name'] = 'aa'
    params_dict['phone'] = '123456789'
    params_dict['tz'] = 'Europe/Berlin'
    create_new_user(params_dict)



@login_manager.user_loader
def load_user(userid):
    # logger.debug('# userid is: '+str(userid))
    return User(userid)
# initialise the flask_login


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/device/<client_name>', methods=['GET', 'POST'])
@login_required
def device_single(client_name):
    return render_template('dash_device_single.html', current_username=current_user.name, client_name=client_name)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def device_dashx():
    return render_template('dash_devices.html')  # , client_name=client_name)


# Devices overview table - route
@app.route('/devices', methods=['GET', 'POST'])
@login_required
def devices():
    return render_template('dash_devices.html', current_username=current_user.name)


@app.route('/device_add', methods=['GET', 'POST'])
@login_required
def device_add():
    try:
        missing_params_list = []

        params_to_fetch = ['client_name']

        params_dict = {}
        for param in params_to_fetch:

            param_val = request.form.get(param, 0)

            if not param_val:
                missing_params_list.append(param)

            else:
                params_dict[param] = param_val

        logger.debug('# params_dict: '+str(params_dict) +
                     '  missing_params_list: '+str(missing_params_list))

        if len(missing_params_list) > 0:
            return render_template('missing_params.html', missing_params=missing_params_list)

        #timestr = time.strftime("%Y%m%d_%H%M%S")
        #rand_str = str(random.randint(1000000, 9999999))
        #file_name = timestr + '_' + rand_str + '.pdf'

        client_name = params_dict['client_name']
        device_token = build_token(20)
        client_creation_result = create_new_device(
            client_name, current_user.name, device_token)

        if client_creation_result == False:
            return "The device is already created!"
        else:
            return "The device created successfully! Token: "+str(device_token)

    except Exception as e:
        logger.debug('# exception: '+str(e))


# test - getting the broswer timezone
@app.route("/getTime", methods=['GET'])
def getTime():
    username = current_user.name  # 'a@a.a'
    browsertz = request.args.get("browsertz")
    logger.debug("browser time: %s" % (browsertz))
    #logger.debug("server time : %s" % (time.strftime('%A %B, %d %Y %H:%M:%S')))
    timezone_write(username, browsertz)
    return "Done"

# Devices overview table - data fetcher


@app.route('/api/data')
#@login_required
def table_data():

    username = current_user.name
    #username = 'a@b.c'
    search_like = request.args.get('search[value]')

    # sorting
    order = []
    order_item = {'column_name': '', 'direction': ''}

    i = 0

    # for multi-column sorting
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break

        # order column
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['user_name', 'client_name', 'first_message', 'last_message']:
            col_name = 'last_message'

        # order direction
        if request.args.get(f'order[{i}][dir]') == 'desc':
            direction = 'desc'
        else:
            direction = 'asc'

        order_item['column_name'] = col_name
        order_item['direction'] = direction

        order.append(order_item)
        i += 1

    length = request.args.get('length')
    start = request.args.get('start')

    # res = fetch_device_overview_clickhouse(
    #    'table1', username, search_like, start, length, order)

    res = fetch_device_overview_clickhouse(
        'table1', username, search_like, start, length, order
    )

    res['draw'] = request.args.get('draw', type=int)

    return res


def test_common_prefix():
    return


def sortFn(tpl):
    return tpl[1]


def test_common_prefix():
    """
    The function to test the common prefix function.__base__
    """
    # test 1
    # write the mqtt data write to mongodb

    return


@app.route('/fetchdata', methods=["GET", "POST"])
#@login_required
def fetchdata():

    client_name = request.args.get('client_name', None)

    limit = 30

    parameter_list = ['param1', 'param2']

    data_to_revert = {}

    # the "current_user.name" identifies the user. This way the data for only this user is reverted back to js code in browser to render.
    for param_name in parameter_list:
        res = fetch_data_per_param(user_name=str(
            current_user.name), client_name=client_name, param_name=param_name, limit=limit)
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

    #logger.debug('')
    #logger.debug('# request.form: %s', str(request.form))
    #logger.debug('# request.args: %s', str(request.args))
    #logger.debug('# request.args.get("next"): ' +
    #             str(request.args.get("next")))

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
            login_user(User(email), remember=remember_me_flag)
            return redirect(next or url_for('devices'))
        else:
            return render_template('login.html', login_message='The password is not correct!')

    else:

        return render_template('login.html', login_message="Sign in to continue...")


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    #logger.debug('in flask, route is /signup, method: ' + str(request.method))

    #logger.debug('')
    #logger.debug('# in signup, request.form: ' + str(request.form))
    #logger.debug('# in signup, request.args: ' + str(request.args))
    #logger.debug('# in signup, request.args.get("next"): ' +
    #             str(request.args.get("next", '')))

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

        # country = request.form.get('country', None)
        new_user_data = {
            'email': email,
            'password': password_main,
            'agreeterms': agreeterms,
            'time-formatted': dt.now().strftime("%Y-%m-%d %H:%M:%S"),
            'time': dt.now()
        }
        

        new_user_data_in_separate_lines = json.dumps(new_user_data, indent=4)
        # message_dict = {'email': email,
        #                'confirmation_link': 'https://www.qlines.net/confirmation/wertgwekjnekrg'}

        logger.debug(
            '# going to create mongodb entry for a new user creation with info: '+str(new_user_data_in_separate_lines))
        create_user_result = create_new_user(new_user_data)
        logger.debug('# mongodb create_new_user result: ' +
                     str(create_user_result))

        if create_user_result:
            # notify admin about the creation of new user
            email_result = enqueue_long_running_function(
                send_general_text_email, new_user_data_in_separate_lines, 'New user registered')
            logger.debug(
                '# email_result from submitting to redis: ' + str(email_result))

            return render_template('confirm_registration.html')

        else:
            return render_template('signup.html', message='The user already exists!')

        # todo: enable email confirmation for sign up requests, for the moment, for MVP it is not necessary,
        # send_email_signup(message_dict)

    else:
        return render_template('signup.html', message='Signing up is easy. It only takes a few steps')


# @app.route('/pricing', methods=['GET', 'POST'])
# def pricing():
#     logger.debug('in flask, route is /pricing')
#     return render_template('pricing.html')


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

        #email_result = q.enqueue(send_email_contact, message_dict)
        email_result = enqueue_long_running_function(
            send_email_contact, message_dict)
        logger.debug(
            '# email_result from submitting to redis: ' + str(email_result))

        if email_result:
            result = 'Your message sent successfully. Thank you!'

    return render_template('contact.html', result=result)



@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)

    # to restart the flask when template htmls or static files are changed
    from os import path, walk
    extra_dirs = ['./templates/', './static/']
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)

    app.run(extra_files=extra_files, host='0.0.0.0', port=5000, debug=True)
