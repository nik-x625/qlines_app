# Logging
import logging
import logging.config

# Flask
import flask
import flask_login
from flask import Flask, render_template, json, jsonify, request, make_response, current_app, abort

# Mongo
from mongodb_module import *

# Others
import time
from datetime import datetime
from email_module import send_email
import subprocess


# App initialisation
app = Flask(__name__)
app.secret_key = 'somekey'


# Logger initialisations
logging.config.fileConfig(fname='logging_config.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger(__name__)



############### flask_login initialisation ###############
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in read_user_doc(username)['username']:
        return

    user = User()
    user.id = username
    return user
############### flask_login initialisation ###############



@app.route('/', methods=['GET', 'POST'])
def dashboard():
    app.logger.debug('xxx')
    return render_template('dashboard.html')

@app.route('/nav_home', methods=['GET', 'POST'])
def nav_home():
    return render_template('nav_home.html')


# used to turn on/off the asterisk PBX on the same VPS. The PBX is for relaying the VoIP service.
@app.route('/switch_asterisk')
def switch_asterisk():
    try:
        request_type = request.args.get('request_type', 0, type=str)

        app.logger.debug('# request_type: '+str(request_type))

        if request_type == 'switch_on':
            cmd = './asterisk_start'
            subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            return jsonify(result='Start requested!')

        elif request_type == 'switch_off':
            cmd = './asterisk_stop'
            subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            return jsonify(result='Stop requested!')

        elif request_type == 'check_status':
            cmd = 'ps -ef | grep asterisk | grep -v "grep asterisk"'
            res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            out, error = res.communicate()
            if not out:
                out = 'Turned off!'
            if 'asterisk -p -U asterisk' in out:
                out = 'Turned on!  -  ' + out
            return jsonify(result='Status is: '+str(out))

        else:
            return jsonify(result='The request is not valid')

        # return jsonify(result='done in switch_asterisk from flask')
    except Exception as e:
        return str(e)

'''

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    result = ''
    logger.debug('in contact function 7')
    if flask.request.method == 'POST':

        logger.debug('thats post method')
        name = flask.request.form['name']
        email = flask.request.form['email']
        message = flask.request.form['message']

        doc = {'name': name,
               'email': email,
               'message': message,
               'datetime': datetime.now()}

        # mongo_result = contact_submission_update(doc)

        logger.debug('sending email')
        email_result = send_email('submitted form', str(doc))

        # submission_result = mongo_result and email_result

        # logger.debug('mongo_result: '+str(mongo_result))
        logger.debug('email_result: ' + str(email_result))

        if email_result:
            result = 'Your message submitted successfully!'

    return render_template('contact.html', result=result)


@app.route('/contact_form_submission', methods=['POST'])
def contact_form_submission():
    name = flask.request.form['name']
    email = flask.request.form['email']
    message = flask.request.form['message']

    logger.debug('# in function contact_form_submission')

    # contact_submission_update({'name': name,
    #                           'email': email,
    #                           'message': message,
    #                           'datetime': datetime.now()})

    return 'Ok'


@app.route('/cloud_manager', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':

        try:
            logger.debug("Get received !!!")
        except Exception as e:
            logger.debug("Error to print of external: " + str(e))
        return render_template('cloud_manager_login.html')

    username = flask.request.form['username']
    logger.debug('username: ' + str(username))

    user_from_db = read_user_doc(username)
    logger.debug('user_from_db: ' + str(user_from_db))

    try:
        if flask.request.form['password'] == user_from_db['password']:
            logger.debug("the condition is satis!")
            user = User()
            user.id = username
            flask_login.login_user(user)
            logger.debug(
                "going to return   flask.redirect(flask.url_for('home_protected')) ")
            return flask.redirect(flask.url_for('home_protected'))
    except Exception as e:
        logger.debug('Exception in login: ' + str(e))
        return '<p>Username Invalid</p><a href="./">Login</a>'
    return '<p>Password Invalid</p><a href="./">Login</a>'


# Logout function
@app.route('/logout')
def logout():
    flask_login.logout_user()
    # return '<p>Logged out</p><a href="./">Login</a>'
    # return render_template('login.html')
    return flask.redirect(flask.url_for('login'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/cpeList', methods=['POST', 'GET'])
def create_cpe_func():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/update_data', methods=['POST'])
def update_data():
    logger.debug('# reached to route function update_data with request.data: '+str(request.data))

    if not request.data:
        abort(400)

    datastring = request.data  # .replace("'", "\"")
    logger.debug('# datastring sent: '+str(datastring))
    dict = json.loads(datastring)
    cpe_public_ip = request.remote_addr
    current_time = datetime.now()
    dict['cpe_public_ip'] = cpe_public_ip
    dict['upload_time'] = current_time

    logger.debug('# CPE uploaded this dict to go in db now is: ' +str(dict))

    # if not 'cpeid' in dict.keys():
    #    return jsonify({'code': 400, 'message': 'Need cpeid to add or update the device in DB'})

    # push the posted data to DB
    update_sensor_data(dict)

    return jsonify({'code': 200, 'message': 'Request is accepted in REST API'})
'''

if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=8080, debug=True)
