#!/bin/python3
import re

from flask import Flask, send_from_directory, send_file
from flask import request
from flask import session

from datetime import datetime, timedelta

# seconds to count down
PLAYTIME=120

app = Flask(__name__)
app.secret_key = b'super_secret_stuff2'

scores = dict()
endtime = datetime.now() + timedelta(seconds=PLAYTIME)


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
    name = re.sub('/[^a-z0-9 \.,_-]', "", name)
    new_score = re.sub('/[^a-z0-9 \.,_-]', "", new_score)

    if name in scores:
        if scores[name] < int(new_score):
            scores[name] = int(new_score)
    else:
        scores[name] = int(new_score)
    return '', 201


def seconds_until_end():
    return max((endtime - datetime.now()).total_seconds(), 0.0)

@app.route('/intro/start', methods=["POST"])
def start_timer():
    endtime = datetime.now() + timedelta(seconds=PLAYTIME)
    return str(seconds_until_end()), 201

@app.route('/intro/seconds_left', methods=["GET"])
def seconds_left():
    return str(seconds_until_end()), 200


@app.route('/intro/game', methods=["GET"])
def get_game():
    return send_file('data/index.html', as_attachment=True)


if __name__ == '__main__':
    app.run()
