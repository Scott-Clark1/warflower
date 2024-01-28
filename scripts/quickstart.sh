export FLASK_APP='./warflower/webapp/main.py'
flask run &> flask.log &
PYTHONPATH='./client' python client/keanu/bot.py &> bot.log &
