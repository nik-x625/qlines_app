#!/usr/bin/python
import logging
import logging.config
import flask
from flask import Flask, render_template, json, jsonify, request, make_response, current_app, abort
from mongodb_module import *
import time
from datetime import datetime
from email_module import *
from flask import render_template, make_response


app = Flask(__name__)
app.secret_key = 'somekey'

logging.config.fileConfig(fname='logging_config.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_clean():
    return render_template('index.html')


@app.route('/search_backend', methods=['GET', 'POST'])
def add_numbers():

    if flask.request.method == 'POST':

        page = flask.request.form.get('page', 1)

        print('flask username:' +str(flask.request.form.get('user',None)))
        print('flask keyword:' +str(flask.request.form))

        print('in search_backend, page: '+str(page))

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
        ]
        return render_template('search_result.html', results=results)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=8080, debug=True)
