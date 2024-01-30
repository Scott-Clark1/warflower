from flask import Flask, jsonify, request
from flask_httpauth import HTTPTokenAuth
import os
import yaml

import logging

from warflower.controller import ServerManager


app = Flask("webapp")

file_handler = logging.FileHandler('/home/warflower/logs/flask.log', encoding='utf-8', mode='w+')
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info("Starting up!")
app.logger.warning("Starting up warning!")

auth = HTTPTokenAuth(scheme='Bearer')

secrets = yaml.safe_load(open(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "tokens.secret.yaml"
  )))


MGMT = ServerManager()

@auth.verify_token
def verify_token(token):
  if token in secrets:
    return secrets[token]["name"]


@app.route('/list')
@auth.login_required
def list_configs():
  granularity = request.args.get('g', 'configs')

  if granularity == 'configs':
    return jsonify({"status" : 200, "data" : MGMT.list_configs()})
  elif granularity == 'games':
    return jsonify({"status" : 200, "data" : MGMT.list_games()})
  else:
    return jsonify({"status" : 400})



@app.route('/start/<serverid>', methods=['POST'])
@auth.login_required
def start_server(serverid):
  res = MGMT.start_server(serverid)
  if res:
    return jsonify({"status" : 200, "ok" : True})
  return jsonify({"status" : 500, "ok" : False})

@app.route('/stop/<serverid>', methods=['POST'])
@auth.login_required
def stop_server(serverid):
  res = MGMT.stop_server(serverid)
  if res:
    return jsonify({"status" : 200, "ok" : True})
  return jsonify({"status" : 500, "ok" : False})


if __name__ == '__main__':
  # starting app
  app.run(debug=True, host='0.0.0.0')
