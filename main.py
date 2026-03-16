from datetime import datetime
from flask import Flask, redirect, render_template, request, jsonify, url_for
import queries
from dataclasses import dataclass

@dataclass
class DoodleVote:
    date: datetime
    count_votes: int

app = Flask(__name__)
# This removes the strict slash requirement for the entire app
app.url_map.strict_slashes = False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/users/<user_id>", methods=["GET"])
def user_home(user_id):
    user = queries.get_user_by_id(user_id)
    return render_template("index.html", user=user)

@app.route("/users", methods=["POST"])
def create_user():
    email = request.form["email"]
    queries.create_user("max", email, "")
    user = queries.get_user_by_email(email)
    return redirect(url_for("get_appointments", user_id=user.id))

@app.route("/users/<user_id>/appointments", methods=["POST"])
def create_appointment(user_id):
    queries.create_appointment("title", user_id, 1)
    return redirect("/users/<user_id>/appointments", code=302)

@app.route("/users/<user_id>/appointments", methods=["GET"])
def get_appointments(user_id):
    appointments = []
    for appointment in queries.get_all_appointments():
        if appointment.user_id == int(user_id):
            appointments.append(appointment)
    for attendance in queries.get_attendances_by_user_id(user_id):
            appointment = queries.get_appointment_by_id(attendance.appointment_id)
            if appointment not in appointments:
                appointments.append(appointment)
    return render_template("show_events.html", user_id=user_id, appointments=appointments)

@app.route("/appointments/showall", methods=["GET"])
def show_all_appointments():
    appointments = []
    for appointment in queries.get_all_appointments():
        appointments.append(appointment)
    return jsonify(appointments)

@app.route('/users/<user_id>/appointments/<appointment_id>', methods=['POST', 'GET'])
def get_appointment(appointment_id):
    return str(queries.get_appointment_by_id(appointment_id).id)

@app.route('/appointments/<appointment_id>/create_doodle', methods=['POST'])
def create_doodle(appointment_id):
    poll_description = "test poll"   # request.form["poll_description"]
    poll = queries.create_poll(appointment_id, poll_description)
    doodle_dates = []
    doodle_dates.append(request.form["date1"])
    doodle_dates.append(request.form["date2"])
    doodle_dates.append(request.form["date3"])
    for doodle_date in doodle_dates:
        queries.create_choice(poll.id, doodle_date)
    return redirect("/appointments/<appointment_id>/show_doodle", code=302)

@app.route('/appointments/<appointment_id>/show_doodle', methods=['GET'])
def show_doodle(appointment_id):
    options = []
    poll_id = queries.get_poll_by_id(appointment_id).id
    choices = queries.get_choices_by_poll_id(poll_id)
    for choice in choices:
        votes = queries.get_votes_by_choice(choice.id)
        numVotes = len(votes)
        options.append(DoodleVote(choice.label, numVotes))
    return render_template("doodle.html", options=options)

@app.route('/users/<user_id>/appointments/<appointment_id>/vote', methods=['POST'])
def create_vote(user_id, appointment_id):
    pass

if __name__ == '__main__':
    app.run(debug=True)
