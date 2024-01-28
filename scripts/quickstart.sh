export FLASK_APP='./warflower/webapp/main.py'
PYTHONPATH='./' python $FLASK_APP &> flask.log &
PYTHONPATH='./client' python client/keanu/bot.py &> bot.log &
