#!/usr/bin/python
import logging
import logging.config
import time
import os

from flask import Flask, render_template, json, jsonify, request, make_response, current_app
from flask import abort, render_template, make_response, Flask, render_template, request, current_app
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


@app.route('/', methods=['GET', 'POST'])
def main_clean():
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


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=8080, debug=True)
