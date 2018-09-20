from flask import Flask
from flask import request
from flask import session
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'super_secret_stuff'


@app.route('/')
def hello_world():
    scores = {"noone": 5}
    session['scores'] = scores
    return 'Hello World!'


@app.route('/scores', methods=["GET"])
def get_scores():
    scores = session['scores']
    sorted_scores = sorted(scores.items(), key=lambda e: -e[1])[:10]
    return str(sorted_scores)


@app.route('/scores', methods=["POST"])
def post_score():
    scores = session['scores']
    new_score = request.form['score']
    name = request.form['name']
    scores[name] = new_score
    session['scores'] = scores
    return 0


@app.route('/start', methods=["POST"])
def start_timer():
    app.config['ENDTIME'] = datetime.now()
    return 0


@app.route('/game', methods=["GET"])
def get_game():
    return 0


if __name__ == '__main__':
    app.run()
