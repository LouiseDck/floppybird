#!/bin/python3
from flask import Flask, send_from_directory, send_file
from flask import request
from flask import session

from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = b'super_secret_stuff2'

scores = dict()
endtime = datetime.utcnow() + timedelta(seconds=300)


@app.route('/intro/')
def hello_world():
    return 'Hello World!'


@app.route('/intro/scores', methods=["GET"])
def get_scores():
    sorted_scores = sorted(scores.items(), key=lambda e: -e[1])[:10]
    sstring = "<table>"
    for score in sorted_scores:
        sstring += "<tr><td>" + str(score[0])
        sstring += "</td><td>" + str(score[1]) + "</td>"
    sstring += "</table>"
    return sstring


@app.route('/intro/scores', methods=["POST"])
def post_score():
    new_score = request.form['score']
    name = request.form['name']
    if name in scores and scores[name] < int(new_score):
        scores[name] = int(new_score)
    return '', 201


@app.route('/intro/start', methods=["POST"])
def start_timer():
    endtime = datetime.now() + timedelta(seconds=120)
    return 0

@app.route('/intro/seconds_left', methods=["GET"])
def seconds_left():
    return min((endtime - datetime.now()).total_seconds(), 0)


@app.route('/intro/game', methods=["GET"])
def get_game():
    return send_file('data/index.html', as_attachment=True)


if __name__ == '__main__':
    app.run()
