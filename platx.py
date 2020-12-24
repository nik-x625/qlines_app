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
    return render_template('index_basic.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    logger.debug('# in search method ' + str())
    
    if flask.request.method == 'POST':
        logger.debug('# in search method, the POST is sent')
        print('name is: ', flask.request.form['the_input'])

    return render_template('index_basic.html')


@app.route('/_add_numbers', methods=['GET', 'POST'])
def add_numbers():
    #a = request.args.get('a', 0, type=int)
    #b = request.args.get('b', 0, type=int)

    #headers = {'Content-Type': 'text/html'}
    print('in add_numbers')

    return "<div style='border: solid blue'><h4>from flask 1</h4><p>from flask 2</p></div>"


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=8080, debug=True)
