from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "psst"

debug = DebugToolbarExtension(app)

responses = []
title = satisfaction_survey.title
instructions = satisfaction_survey.instructions
questions = satisfaction_survey.questions
curr_question = 0


@app.route("/")
def begin_survey():
    """When the user goes to the root route, render a page that shows the user the title of the survey, the instructions, and a button to start the survey"""
    return render_template("/index.html", title=title, instructions=instructions)

@app.route("/answer", methods=["POST"])
def record_answer():
    """Record the user's answer to the question and add value to responses list before redirecting user either to the next question (if there are questions remaining) or to a thank you page (if the user has answered all questions)"""
    global curr_question
    answer = request.form.get(str(curr_question))
    responses.append(answer)
    curr_question += 1
    if curr_question < len(questions):
        return redirect(f"/questions/{curr_question}")
    else: 
        return redirect("/thanks")


@app.route("/questions/<int:question_number>")
def show_question(question_number):
    """Directs user to page containing the question and a form with the corresponding choices. If a user attempts to access questions out-of-order or access a question that does not exist, they will be redirected to the page of the next unanswered question and alerted via flash message."""
    global curr_question
    question_number = question_number
    if question_number != curr_question:
        flash("Oops! You're trying to access an invalid question! Redirected you to the right one :)")
        return redirect(f"/questions/{curr_question}")
    else:
         return render_template("questions.html",question_number=question_number,question=questions[question_number].question, choices=questions[question_number].choices)

@app.route("/thanks")
def say_thanks():
    """Displays a message thanking the user for taking the survey."""
    return render_template("thanks.html")