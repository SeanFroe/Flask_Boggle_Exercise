
from flask import Flask, request, render_template, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'boggle'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def homepage():
    '''Start page of Boggle'''

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    return render_template('index.html', board=board,
                           highscore=highscore,
                            nplays=nplays )

@app.route("/check-word")
def check_word():
    '''Check if word is in dictionary.'''

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board,word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    ''' Receive score, update nplays, update high score if appropriate. '''

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
