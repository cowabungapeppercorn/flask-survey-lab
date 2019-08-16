from flask import Flask, request, render_template, redirect, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "we need secrets"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

chosen_survey = surveys['satisfaction']


@app.route('/')
def index():
    "Displays basic survey information on index"

    return render_template('home.html',
                           survey_title=chosen_survey.title,
                           survey_instructions=chosen_survey.instructions)


@app.route('/', methods=['POST'])
def start_session():
    session['responses'] = []

    return redirect('/questions/0')


@app.route('/questions/<int:question_num>')
def question(question_num):
    session_responses = session['responses']
    "Makes sure user is going to the right question"
    if len(session_responses) >= len(chosen_survey.questions):
        flash("YEAH I BET YOU WANNA CHANGE YOUR ANSWERS")
        return redirect('/thanks')
    elif not question_num == len(session_responses):
        flash("JUST ANSWER THE QUESTIONS IN ORDER BRO!!!")
        return redirect(f'/questions/{len(session_responses)}')

    "Displays a question and choices from a survey"

    question = chosen_survey.questions[question_num]

    return render_template('question.html',
                           question=question,
                           survey_title=chosen_survey.title)


@app.route('/answer', methods=["POST"])
def record_response():
    "Takes user's response and puts it into responses list"

    session_responses = session['responses']
    response = request.form["question"]
    session_responses.append(response)
    session['responses'] = session_responses

    if len(session_responses) == len(chosen_survey.questions) or \
       len(session_responses) > len(chosen_survey.questions):
        return redirect('/thanks')
    else:
        return redirect(f'/questions/{len(session_responses)}')


@app.route('/thanks')
def thanks():
    "Thanks the user for being a survey sheep."

    return render_template('thanks.html')
