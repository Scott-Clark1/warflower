from flask import Flask, jsonify
from flask_httpauth import HTTPTokenAuth
import yaml

from warflower.controller import ServerManager


mgmt = ServerManager()

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

secrets = yaml.safe_load(open("./tokens.secret.yaml"))

@auth.verify_token
def verify_token(token):
  if token in secrets:
    return tokens[secrets]["name"]

@app.route('/test')
@auth.login_required
def hello_world():
	return "Hello, {}!".format(auth.current_user())


@app.route('/list')
@auth.login_required
def list_configs():
	return jsonify({mgmt.list_configs()})



if __name__ == '__main__':
  # starting app
  app.run(debug=True,host='0.0.0.0')
