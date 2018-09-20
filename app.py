#!/bin/python3
import re

from flask import Flask, send_from_directory, send_file, redirect
from flask import request
from flask import session

from datetime import datetime, timedelta

# seconds to count down
PLAYTIME=120

app = Flask(__name__, static_folder='public')
app.secret_key = b'super_secret_stuff2'

scores = {"Rien": 3}
endtime = datetime.now() + timedelta(seconds=PLAYTIME)




@app.route('/intro/scores', methods=["GET"])
def get_scores():
    # scores = {'ding': 0, 'ander':10}
    sorted_scores = sorted(scores.items(), key=lambda e: -e[1])[:10]
    left = int(seconds_until_end())
    sstring = "<html><head><title>" + str(left) + "</title>"
    sstring += "<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" \
               "\"> <script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js\"></script> " \
               "<script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"></script> "
    if left > 0:
        sstring += "<meta http-equiv='refresh' content='1'>"
    else:
        sstring += "<meta http-equiv='refresh' content='5;url=https://stuw.ugent.be'>"
    sstring += "</head><body>"
    if len(sorted_scores) > 0:
        cur_win = sorted_scores[0][0]
    else:
        cur_win = "No one"
    sstring += "<div class=\"jumbotron jumbotron-fluid\">" \
                "<div class=\"container\">" \
                "<h1 class=\"display-1\">Speel mee op <a>https://stuw.ugent.be/intro/</a></h1>" \
                "<h1 class=\"display-4\">Huidige winnaar: " + str(cur_win) + "</h1>" \
                "</div>" \
                "</div>"

    sstring += "<table class=\"table table-striped\">"
    sstring += "<thead class=\"thead-dark\"> <tr> <th scope=\"col\">#</th> <th scope=\"col\">Naam</th><th scope=\"col\">Score</th></tr> </thead> <tbody>"
    for c, score in enumerate(sorted_scores):
        sstring += "<tr><th scope=\"row\">" + str(c) + "</th>"
        # sstring += "<tr><td>" + str(c)
        sstring += "</td><td>" + str(score[0]) + "</td>"
        sstring += "</td><td>" + str(score[1]) + "</td></tr>"
    sstring += "</tbody></table></body></html>"
    return sstring


@app.route('/intro/scores', methods=["POST"])
def post_score():
    new_score = request.form['score']
    name = request.form['name']
    name = re.sub('/[^a-zA-Z0-9 \.,_-]', "", name)
    name = name[:64]
    new_score = re.sub('/[^0-9 \.,_-]', "", new_score)

    if name in scores:
        if scores[name] < int(new_score):
            scores[name] = int(new_score)
    else:
        scores[name] = int(new_score)
    return '', 201


def seconds_until_end():
    global endtime
    return max((endtime - datetime.now()).total_seconds(), 0.0)

@app.route('/intro/start', methods=["POST"])
def start_timer():
    global endtime
    endtime = datetime.now() + timedelta(seconds=PLAYTIME)
    return str(seconds_until_end()), 201

@app.route('/intro/seconds_left', methods=["GET"])
def seconds_left():
    return str(seconds_until_end()), 200


@app.route('/intro/supersecretstartbutton', methods=["GET"])
def secret_start():
    return "<form action='/intro/start' method='post'><button name='foo' value='go'>Start</button></form>"

@app.route('/intro/game', methods=["GET"])
def get_game():
    return send_file('data/index.html', as_attachment=True)

@app.route('/intro/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)


if __name__ == '__main__':
    app.run()
