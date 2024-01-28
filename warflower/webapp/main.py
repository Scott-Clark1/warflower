from flask import Flask, jsonify
from flask_httpauth import HTTPTokenAuth
import os
import yaml

from warflower.controller import ServerManager


mgmt = ServerManager()

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

secrets = yaml.safe_load(open(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "tokens.secret.yaml"
  )))

@auth.verify_token
def verify_token(token):
  if token in secrets:
    return secrets[token]["name"]

@app.route('/test')
@auth.login_required
def hello_world():
  return "Hello, {}!".format(auth.current_user())


@app.route('/list')
@auth.login_required
def list_configs():
  return jsonify({"status" : 200, "data" : mgmt.list_configs()})


@app.route('/start/<serverid>', methods=['POST'])
@auth.login_required
def start_server(serverid):
  res = mgmt.start_server(serverid)
  if res:
    return jsonify({"status" : 200, "ok" : True})
  return jsonify({"status" : 500, "ok" : False})

@app.route('/stop/<serverid>', methods=['POST'])
@auth.login_required
def stop_server(serverid):
  res = mgmt.stop_server(serverid)
  if res:
    return jsonify({"status" : 200, "ok" : True})
  return jsonify({"status" : 500, "ok" : False})


if __name__ == '__main__':
  # starting app
  app.run(debug=True,host='0.0.0.0')
