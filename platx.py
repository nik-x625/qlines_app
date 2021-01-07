#!/usr/bin/python
import logging
import logging.config
import os
import time
from datetime import datetime

import flask
import flask_login
import redis
from flask import *
from flask import (Flask, Response, abort, current_app, json, jsonify,
                   make_response, redirect, render_template, request, session,
                   url_for)
from flask_login import (LoginManager, UserMixin, login_required, login_user,
                         logout_user)
from rq import Queue

from email_module import *
from flask_pager import Pager
from mongodb_module import *

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







# initialise the flask_login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

# create some users with ids 1 to 5
users = [User(id) for id in range(1, 5)]



# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    print()
    print('# request.form: '+str(request.form))
    print('# request.args: '+str(request.args))
    print('# request.args.get("next"): '+str(request.args.get("next")))
    if request.method == 'POST':
            email = request.form.get('email_holder',None)
            password = request.form.get('password_holder',None)
            keepsignedin = request.form.get('keepsignedin_holder',None)

            
            if keepsignedin == "on":
                remember_me_flag = True
            else:
                remember_me_flag = False

            # do user/pass verification here
            if 1: # if verification passed

                next = request.args.get('next')

                login_user(User(2), remember=remember_me_flag)
                return redirect(next or url_for('dashboard')) #
            else:
                return abort(401)
    else:

        return render_template('login.html')



# somewhere to logout
@app.route("/logout")
def logout():
    logout_user()
    return render_template('index.html')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)





@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')





@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# test only
users = {'foo@bar.tld': {'password': 'secret'}}


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




if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=8080, debug=True)
