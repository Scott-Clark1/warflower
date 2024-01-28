from flask import Flask
app = Flask(__name__)

@app.route('/test')
def hello_world():
    return "Hello, World!"



if __name__ == '__main__':
  # starting app
  app.run(debug=True,host='0.0.0.0')
