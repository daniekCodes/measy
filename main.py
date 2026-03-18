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
'''
@app.route("/users/<user_id>", methods=["GET"])
def user_home(user_id):
    user = queries.get_user_by_id(user_id)
    events = []
    invitations = []
    for appointment in queries.get_all_appointments():
        if appointment.user_id == int(user_id):
            events.append(appointment)
    for attendance in queries.get_attendances_by_user_id(user_id):
            appointment = queries.get_appointment_by_id(attendance.appointment_id)
            invitations.append(appointment)
    return render_template("home.html", user=user, events=events, invitations=invitations)
'''


@app.route("/users/<user_id>", methods=["GET"])
def user_home(user_id):
    # --- Dummy daten---

    dummy_user = {"id": user_id, "name": "Test User"}

    dummy_events = [
        {"id": 1, "title": "Projekt Meeting", "start_datetime": "20.03.2026 10:00"},
        {"id": 2, "title": "Team Lunch", "start_datetime": "22.03.2026 12:30"}
    ]

    dummy_invitations = [
        {"id": 3, "title": "Kundenpräsentation", "start_datetime": "25.03.2026 14:00"},
        {"id": 4, "title": "Weihnachtsfeier", "start_datetime": "15.12.2026 18:00"}
    ]

    return render_template(
        "home.html",
        user=dummy_user,
        events=dummy_events,
        invitations=dummy_invitations
    )

def create_user():
    email = request.form["email"]
    queries.create_user("max", email, "")
    user = queries.get_user_by_email(email)
    return redirect(url_for("get_appointments", user_id=user.id))

@app.route("/users/<user_id>/appointments", methods=["POST"])
def create_appointment(user_id):
    title = request.form["title"]
    description = request.form["description"]
    date_start = datetime.now()
    queries.create_appointment(title, int(user_id), 1,description,date_start)
    return redirect(url_for("user_home", user_id=user_id))
    #redirect(url_for("get_appointments", user_id=user_id))

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

@app.route('/users/<user_id>/appointments/<appointment_id>', methods=['GET'])
def get_appointment(user_id, appointment_id):
    appointment = queries.get_appointment_by_id(appointment_id)
    attendances = queries.get_attendances_by_user_id(appointment_id)
    for attendance in attendances:
        if attendance.appointment_id == appointment_id:
            appointment = attendance
    options = show_doodle(appointment.id)
    return render_template("event_details.html", event=appointment, options=options)

@app.route('/users/<user_id>/appointments/create', methods=['GET'])
def new_appointment(user_id):
    return render_template("create_appointment.html", user_id=user_id)



@app.route('/users/<user_id>/appointments/<appointment_id>/create_doodle', methods=['POST'])
def create_doodle(appointment_id):
    poll_description = "test poll"   # request.form["poll_description"]
    poll = queries.create_poll(appointment_id, poll_description)
    doodle_dates = []
    doodle_dates.append(request.form["date1"])
    doodle_dates.append(request.form["date2"])
    doodle_dates.append(request.form["date3"])
    for doodle_date in doodle_dates:
        queries.create_choice(poll.id, doodle_date)
    return redirect("/users/<user_id>/appointments/<appointment_id>")

def show_doodle(appointment_id):
    options = []
    poll_id = queries.get_poll_by_id(appointment_id).id
    choices = queries.get_choices_by_poll_id(poll_id)
    for choice in choices:
        votes = queries.get_votes_by_choice(choice.id)
        numVotes = len(votes)
        options.append(DoodleVote(choice.label, numVotes))
    return options

@app.route('/users/<user_id>/appointments/<appointment_id>/vote', methods=['POST'])
def create_vote(user_id, appointment_id):
    pass

if __name__ == '__main__':
    app.run(debug=True)
