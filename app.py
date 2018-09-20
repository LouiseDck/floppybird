from flask import Flask, send_from_directory, send_file
from flask import request
from flask import session

from datetime import datetime

app = Flask(__name__)
app.secret_key = b'super_secret_stuff2'

scores = dict()
endtime = 0


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/scores', methods=["GET"])
def get_scores():
    sorted_scores = sorted(scores.items(), key=lambda e: -e[1])[:10]
    sstring = "<table>"
    for score in sorted_scores:
        sstring += "<tr><td>" + str(score[0])
        sstring += "</td><td>" + str(score[1]) + "</td>"
    sstring += "</table>"
    return sstring


@app.route('/scores', methods=["POST"])
def post_score():
    new_score = request.form['score']
    name = request.form['name']
    scores[name] = int(new_score)
    return '', 201


@app.route('/start', methods=["POST"])
def start_timer():
    endtime = datetime.now()
    return 0


@app.route('/game', methods=["GET"])
def get_game():
    return send_file('data/index.html', as_attachment=True)


if __name__ == '__main__':
    app.run()
