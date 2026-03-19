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
    events = []
    invitations = []
    for appointment in queries.get_all_appointments():
        if appointment.user_id == int(user_id):
            events.append(appointment)
    for attendance in queries.get_attendances_by_user_id(user_id):
            appointment = queries.get_appointment_by_id(attendance.appointment_id)
            invitations.append(appointment)
    return render_template("home.html", user_id=user_id, events=events, invitations=invitations)

@app.route("/users", methods=["POST"])
def create_user():
    email = request.form["email"]
    queries.create_user("max", email, "")
    user = queries.get_user_by_email(email)
    return redirect(url_for("get_appointments", user_id=user.id))

@app.get("/users")
def get_all_users():
    users = queries.get_all_users()
    tmp_str = ""
    for user in users:
        tmp_str += f"{user.id}. Name: {user.name} Email: {user.email}\n"
    return tmp_str

@app.route("/users/<user_id>/appointments", methods=["POST"])
def create_appointment(user_id):
    title = request.form["title"]
    description = request.form["description"]
    date_start = None
    date_end = None

    if request.form["fixed_date"]:
        date_start = datetime.fromisoformat(f"{request.form["fixed_date"]}T{request.form["fixed_start_time"]}")
        date_end = datetime.fromisoformat(f"{request.form["fixed_date"]}T{request.form["fixed_end_time"]}")

    location_id = None
    meeting_type = request.form["location_type"]

    if meeting_type == "physical":
        location_id = queries.create_location( 
                meeting_type=meeting_type,
                street=request.form["street"],
                house_number=request.form["housenumber"],
                postal_code = request.form["plz"],
                city = request.form["city"])
    else:
        location_id = queries.create_location(
               meeting_type=meeting_type,
               virtual_location = request.form["meeting_link"])

    appointment_id = queries.create_appointment(
            title, 
            int(user_id), 
            location_id,
            description,
            date_start,
            date_end)

    if request.form["option1_date"]:
        options = []
        poll_id = queries.create_poll(appointment_id, "")
        for i in range(1,4):
            option_date = request.form[f"option{i}_date"]
            option_start_time = request.form[f"option{i}_start"]
            option_end_time = request.form[f"option{i}_end"]
            queries.create_choice(poll_id, f"{option_date}T{option_start_time} - {option_date}T{option_end_time}") 

    for user_email in request.form["invite_emails"].split(" "):
        attending_user = queries.get_user_by_email(user_email)
        attending_user_id = None if not attending_user else attending_user.id
        if not attending_user_id:
            user_id = queries.create_user("", user_email, "")
        queries.create_attendance(attending_user_id, appointment_id)

    return redirect(url_for("user_home", user_id=user_id))


@app.route("/users/<user_id>/appointments/<appointment_id>", methods=["POST"])
def delete_appointment(user_id, appointment_id):
    appointment = queries.get_appointment_by_id(appointment_id)
    if appointment == None:
        return appointment_id
    if appointment.user_id == int(user_id):
        queries.delete_appointment(appointment.id)
    return redirect(url_for("user_home", user_id=user_id))

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
    strr = ""
    for appointment in queries.get_all_appointments():
        appointments.append(appointment)
    return appointments

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
    return render_template("create_event.html", user_id=user_id)

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
    # no poll created 
    poll = queries.get_poll_by_id(appointment_id)
    if poll:
        choices = queries.get_choices_by_poll_id(poll.id)
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
