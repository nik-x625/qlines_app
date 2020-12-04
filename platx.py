# Logging
import logging
import logging.config
import flask
from flask import Flask, render_template, json, jsonify, request, make_response, current_app, abort
from mongodb_module import *
import time
from datetime import datetime
from email_module import *

app = Flask(__name__)
app.secret_key = 'somekey'

logging.config.fileConfig(fname='logging_config.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET', 'POST'])
def main_clean():
    return render_template('index_basic.html')

if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=8080, debug=True)
