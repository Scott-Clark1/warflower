from flask import Flask
from flask_httpauth import HTTPTokenAuth
import yaml

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



if __name__ == '__main__':
  # starting app
  app.run(debug=True,host='0.0.0.0')
