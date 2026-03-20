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
            att_appointment = queries.get_appointment_by_id(attendance.appointment_id)
            invitations.append(att_appointment)
    return render_template("home.html", user={"id": user_id}, events=events, invitations=invitations)

@app.route("/users", methods=["POST"])
def create_user():
    email = request.form["email"]
    name = request.form["name"]
    password = request.form["password"]
    queries.create_user(name, email, password)
    user = queries.get_user_by_email(email)
    return redirect(url_for("user_home", user_id=user.id))

@app.get("/users")
def get_all_users():
    users = queries.get_all_users()
    tmp_str = ""
    for user in users:
        tmp_str += f"{user.id}. Name: {user.name} Email: {user.email}\n"
    return tmp_str

@app.route("/users/<user_id>/appointments", methods=["POST"])
def create_appointment(user_id):
    user = queries.get_user_by_id(user_id)
    if not user:
        return render_template("home")
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

    # create attendance for organizer
    queries.create_attendance(user_id, appointment_id)

    # create attendance for all invited users 
    # and create an account for all emails that are not in 
    # db
    if request.form["invite_emails"]:
        for attending_user_email in request.form["invite_emails"].split(" "):
            attending_user = queries.get_user_by_email(attending_user_email)
            attending_user_id = None if not attending_user else attending_user.id
            if not attending_user_id:
                attending_user_id = queries.create_user("", attending_user_email, "")
            queries.create_attendance(attending_user_id, appointment_id)

    return redirect(url_for("user_home", 
            user={"id": user.id, "name": user.name}))

@app.get("/users/<user_id>/attendances")
def get_attendances_for_user(user_id):
    attendances = queries.get_attendances_by_user_id(user_id)
    test_str = ""
    for attendance in attendances:
        test_str += f"[APP:{attendance.appointment_id} - {attendance.status_attend}] ### "
    return test_str

@app.get("/users/<user_id>/appointments/<appointment_id>/details")
def appointment_details(user_id, appointment_id):
    appointment = queries.get_appointment_by_id(appointment_id)
    location = queries.get_location_by_id(appointment.location_id)
    poll = queries.get_poll_by_appointment_id(appointment_id)
    user_attendances = queries.get_attendance_by_user(user_id)
    attendance_status = None
    for user_attendance in user_attendances:
        if user_attendance.appointment_id == appointment_id:
            attendance_status = user_attendance.status_attend
            break
    choices = []
    if poll:
        choices = queries.get_choices_by_poll_id(poll.id)
    votes = []
    for choice in choices:
        all_votes = queries.get_votes_by_choice(choice.id)
        for vote in all_votes:
            if vote.user_id == user_id:
                votes.append(vote)

    return render_template("event-details.html",
                           user_id = user_id,
                           appointment = appointment,
                           location = location,
                           poll = poll,
                           attendance_status = attendance_status,
                           choices = choices,
                           votes = votes)

@app.route("/users/<user_id>/appointments/<appointment_id>", methods=["POST"])
def delete_appointment(user_id, appointment_id):
    appointment = queries.get_appointment_by_id(appointment_id)
    if appointment == None:
        return appointment_id
    if appointment.user_id == int(user_id):
        queries.delete_appointment(appointment.id)
    return redirect(url_for("user_home", user_id=user_id))

@app.route('/users/<user_id>/appointments/<appointment_id>', methods=['GET'])
def get_appointment(user_id, appointment_id):
    appointment = queries.get_appointment_by_id(appointment_id)
    user = queries.get_user_by_id(user_id)
    if not appointment or not user:
        return redirect(url_for("home"))
    organizer = queries.get_user_by_id(appointment.id)
    attendances = queries.get_attendances_by_user_id(appointment_id)
    for attendance in attendances:
        if attendance.appointment_id == appointment_id:
            appointment = attendance
    options = show_doodle(appointment.id)
    location = queries.get_location_by_id(appointment.location_id)
    return render_template("event_details.html", 
                           user={"id": user.id, "name": user.name},
                           event=appointment, 
                           options=options, 
                           location=location,
                           organizer={"name": organizer.name})

@app.get("/users/<user_id>/appointments/<appointment_id>/edit")
def edit_appointment(user_id, appointment_id):
    user = queries.get_user_by_id(user_id)
    appointment = queries.get_appointment_by_id(appointment_id)
    if not user or not appointment:
        return render_template("home")
    return render_template("edit_appointment.html", 
                           user={"id": user.id, "name": user.name},
                           appointment=appointment)

@app.route('/users/<user_id>/appointments/create', methods=['GET'])
def new_appointment(user_id):
    user = queries.get_user_by_id(user_id)
    if not user:
        return render_template(url_for("home"))
    return render_template("create_event.html", user={"id": user.id})

@app.get("/users/<user_id>/appointments/<appointment_id>/Date-fix")
def get_fix_date(user_id, appointment_id):
    appointment = queries.get_appointment_by_id(appointment_id)
    if not appointment:
        return render_template("Date-fix.html")
    if user_id != appointment.user_id:
        return render_template("Date-fix.html")
    poll = queries.get_poll_by_appointment_id(appointment_id)
    if not poll:
        return render_template("Date-fix.html")
    choices = queries.get_choices_by_poll_id(poll.id)
     
    attendances = queries.get_attendances_by_appointment_id(appointment_id)
    num_user_invited = len(attendances)
    voted_options = []
    return 

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
