#!/usr/bin/python

import sys
import flask
import atexit
import os
import json
from logging.config import dictConfig
from flask import Flask
from flask import Response
from flask import jsonify
from flask import request
from flask import abort
from apscheduler.scheduler import Scheduler


# Custom
from handler.ping import healthCheck
from handler.dns_propagation_checker import GetPropagationList
from handler.get_whois import GetWhois

# Logging
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

# Variables


app = Flask(__name__)

# Cron
cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
cron.start()


@cron.interval_schedule(minutes=5)
def happylogging():
    app.logger.info("I am still running")


# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))

# HTTP


@app.route("/")
def index():
    index = healthCheck(message="DNS Propagation Checker API")
    return index


@app.route("/ping")
def ping():
    ping = healthCheck(message="pong")
    return ping


@app.route("/dns-propagation-checker", methods=['POST'])
def givelist():
    # Request json format
    # {
    #   "FQDN" : "",
    #   "DNS RECORD" : ""
    # }
    req_data = request.get_json(force=True)
    if not request.json:
        Message = "Missing JSON data"
        app.logger.info(Message)
        abort(400, Message)
    if request.content_type != 'application/json':
        Message = "Missing content_type"
        app.logger.info(Message)
        abort(400, Message)
    else:
        if ('FQDN' in req_data and 'DNS_Record' in req_data):
            try:
                list = GetPropagationList(
                    req_data['FQDN'], req_data['DNS_Record'])
                app.logger.info((json.dumps(list)))
                response = app.response_class(
                    response=json.dumps(list),
                    status=200,
                    mimetype='application/json'
                )
                return response

            except Exception as e:
                app.logger.error((e))
                return (e)
        else:
            Message = "Could not find FQDN or DNS Record in JSON"
            app.logger.info(Message)
            return (Message)

@app.route("/whois", methods=['POST'])
def getwhois():
        # Request json format
        # {
        #   "FQDN" : ""
        # }
    req_data = request.get_json(force=True)
    if not request.json:
        Message = "Missing JSON data"
        app.logger.info(Message)
        abort(400, Message)
    if request.content_type != 'application/json':
        Message = "Missing content_type"
        app.logger.info(Message)
        abort(400, Message)
    else:
        if ('FQDN' in req_data):
            try:
                list = GetWhois(
                    req_data['FQDN'])
                app.logger.info(str(list))
                response = app.response_class(
                    response=str(list),
                    status=200,
                    mimetype='application/json'
                )
                return response

            except Exception as e:
                app.logger.error((e))
                return (e)
        else:
            Message = "Could not find FQDN"
            app.logger.info(Message)
            return (Message)

if __name__ == '__main__':

    # Start app
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=True)
