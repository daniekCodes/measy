from datetime import datetime, date
from flask import Flask, redirect, render_template, request, jsonify, url_for, abort
import queries
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash
import re

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
            events.append(appointment.__dict__)
            if not appointment.start_datetime and not appointment.end_datetime:
                poll = queries.get_poll_by_appointment_id(appointment.id)
                events[-1]["poll"] = poll
    for attendance in queries.get_attendances_by_user_id(user_id):
            att_appointment = queries.get_appointment_by_id(attendance.appointment_id)
            invitations.append(att_appointment.__dict__)
            poll = queries.get_poll_by_appointment_id(att_appointment.id)
            invitations[-1]["poll"] = poll
    return render_template("home.html", user={"id": user_id}, events=events, invitations=invitations)

@app.route("/users", methods=["POST"])
def create_user():
    email = request.form["email"]
    name = request.form["name"]
    password = request.form["password"]
    password_hash = generate_password_hash(password)
    user = queries.get_user_by_email(email)
    if user:
        if not check_password_hash(user.password, password):
            return redirect(url_for("home"))
    else:
        queries.create_user(name, email, password_hash)
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
            user_id=user.id))

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
    organizer = queries.get_user_by_id(appointment.user_id)
    attendances = queries.get_attendances_by_user_id(user.id)
    attendance_status = None
    for attendance in attendances:
        if attendance.appointment_id == appointment.id:
            # appointment = attendance
            attendance_status = attendance.status_attend
    options = show_doodle(appointment.id)
    location = queries.get_location_by_id(appointment.location_id)
    poll = queries.get_poll_by_appointment_id(appointment.id)
    choices = []
    poll_choices = None
    if poll:
        poll_choices = queries.get_choices_by_poll_id(poll.id)
        for poll_choice in poll_choices:
            votes = queries.get_votes_by_choice(poll_choice.id)
            start_datetime = datetime.fromisoformat(poll_choice.label.split(" - ")[0])
            end_datetime = datetime.fromisoformat(poll_choice.label.split(" - ")[1])
            choices.append(poll_choice.__dict__ | {"start_datetime": start_datetime, "end_datetime": end_datetime})
            for vote in votes:
                if vote.user_id == user.id:
                    choices[-1]["user_voted_yes"] = vote.can_attend

    return render_template("event_details.html", 
                           user={"id": user.id, "name": user.name},
                           event=appointment, 
                           options=options, 
                           location=location,
                           organizer=organizer,
                           poll=poll,
                           choices=choices,
                           attendance_status=attendance_status)

@app.get("/users/<user_id>/appointments/<appointment_id>/edit")
def edit_appointment(user_id, appointment_id):
    user = queries.get_user_by_id(user_id)
    appointment = queries.get_appointment_by_id(appointment_id)
    if not user or not appointment:
        return render_template("home")
    location = queries.get_location_by_id(appointment.location_id)
    poll = queries.get_poll_by_appointment_id(appointment.id)
    choices = []
    if poll:
        pre_choices = queries.get_choices_by_poll_id(poll.id)
        for i, choice in enumerate(pre_choices):
            dts = choice.label.split(" - ")
            try:
                dt_start = datetime.fromisoformat(dts[0])
                dt_end = datetime.fromisoformat(dts[1])
                choices.append(choice.__dict__ | {"date": dt_start.date(),
                                                "start_time": dt_start.time(),
                                                "end_time": dt_end.time()})
            except ValueError:
                continue
        # test_str = ""
        # for choice in choices:
        #     test_str += str(choice)
        # return test_str
    return render_template("edit_event.html", 
                           user={"id": user.id, "name": user.name},
                           event=appointment,
                           location=location,
                           poll=poll,
                           choices=choices)

@app.route('/users/<user_id>/appointments/create', methods=['GET'])
def new_appointment(user_id):
    user = queries.get_user_by_id(user_id)
    if not user:
        return redirect(url_for("home"))
    return render_template("create_event.html", user={"id": user.id})

@app.get("/users/<user_id>/appointments/<appointment_id>/Date-fix")
def set_fixed_date(user_id, appointment_id):
    appointment = queries.get_appointment_by_id(appointment_id)
    user = queries.get_user_by_id(user_id)
    if not appointment:
        abort(403)
    if user.id != appointment.user_id:
        abort(403)
    poll = queries.get_poll_by_appointment_id(appointment_id)
    if not poll:
        abort(403)
    choices = queries.get_choices_by_poll_id(poll.id)
    total_votes = 0
    voted = []
    for i, choice in enumerate(choices):
        votes = queries.get_votes_by_choice(choice.id, can_attend=True)
        voted = voted + [vote.user_id for vote in votes]
        start_datetime = datetime.fromisoformat(choice.label.split(" - ")[0])
        end_datetime = datetime.fromisoformat(choice.label.split(" - ")[1])
        choices[i] = choice.__dict__ | {"votes": len(votes),
                                        "start_datetime": start_datetime,
                                        "end_datetime": end_datetime}
    total_votes = len(set(voted))
    total_invited = None
    attendances = queries.get_attendances_by_appointment_id(appointment_id)
    total_invited = len(attendances)    
    return render_template("date_fix.html", 
                           user={"id": user.id}, 
                           appointment=appointment,
                           choices=choices,
                           total_votes=total_votes,
                           total_invited=total_invited
                           )
     
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
    user = queries.get_user_by_id(user_id)
    appointment = queries.get_appointment_by_id(appointment_id)

    if not user or not appointment:
        return "Forbidden"

    if request.form.get("vote_fixed", None):
        user_attends = True if request.form["vote_fixed"] == "yes" else False
        attendance = None
        attendances = queries.get_attendances_by_user_id(user.id)
        for att in attendances:
            if att.appointment_id == appointment.id:
                attendance = att
        if attendance:
            status_attend = "confirmed" if user_attends else "declined"
            queries.update_attendance(attendance.id, status_attend=status_attend)
    else:
        for key in request.form:
            if key.startswith("choice_"):
                choice_id = key[7:]
                voted_yes = True if request.form[key] == "yes" else False
                votes = queries.get_votes_by_choice(choice_id)
                votes = [vote for vote in votes if vote.user_id == user.id]
                if votes:
                    vote = votes[0]
                    if vote.can_attend != voted_yes:
                        queries.update_vote(vote.id, can_attend=voted_yes)
                else:
                    vote_id = queries.create_vote(user_id, choice_id, voted_yes)
                    vote = queries.get_vote_by_id(vote_id)
    return redirect(url_for("user_home", user_id=user_id))

@app.post("/users/<user_id>/appointments/<appointment_id>/update")
def update_event(user_id, appointment_id):
    user = queries.get_user_by_id(user_id)
    appointment = queries.get_appointment_by_id(appointment_id)
    location = queries.get_location_by_id(appointment.location_id)

    event_title = request.form.get("title", None)
    event_description = request.form.get("description", None)
    queries.update_appointment(appointment.id, title=event_title, description=event_description) 

    # user einladen - todo
    event_invite_emails = request.form.get("invite_emails", None)
    for invite_email in event_invite_emails.split():
        invited_user = queries.get_user_by_email(invite_email)
        if not invited_user:
            invited_user_id = queries.create_user("", invite_email, "")
            invited_user = queries.get_user_by_id(user_id)
        # attendance erzeugen, wenn noch nicht existiert
        attendances = queries.get_attendances_by_user_id(invited_user.id)
        att = [x for x in attendances if x.appointment_id == appointment.id]
        if not att:
            queries.create_attendance(invited_user.id, appointment.id)

    location_type = request.form.get("location_type", None)
    location_street = request.form.get("street", None)
    location_housenumber = request.form.get("housenumber", None)
    location_plz = request.form.get("plz", None)
    location_city = request.form.get("city", None)
    location_meeting_link = request.form.get("meeting_link", None)

    if location_type == "physical":
        queries.update_location(location.id, 
                                meeting_type=location_type,
                                street=location_street,
                                house_number=location_housenumber,
                                postal_code=location_plz,
                                city=location_city)
    else:
        queries.update_location(location.id,
                                meeting_type=location_type,
                                virtual_location=location_meeting_link)

    fixed_date = request.form.get("fixed_date", None)
    fixed_start_time = request.form.get("fixed_start_time", None)
    fixed_end_time = request.form.get("fixed_end_time", None)

    meeting_type = request.form.get("meeting_type", None)

    if fixed_date:
        # Fixes Datum eingegeben
        queries.update_appointment(appointment.id,  
                                   start_datetime=datetime.combine(fixed_date, fixed_start_time),
                                   end_datetime=datetime.combine(fixed_date, fixed_end_time))
    elif meeting_type == "none":
        poll = queries.get_poll_by_appointment_id(appointment.id)
        if poll:
            queries.delete_poll(poll.id)
    else: 
        options = []
        for key in request.form:
            if key.startswith("option"):
                options.append(key)

        for i in range(3):
            option = options[i*3:i*3+3]
            m = re.match("[0-9]+", key[6:])
            m2 = re.match("[0-9]+", key[7:])
            if m:
                start_idx, stop_idx = m.span()
                option_id = option[0][6:][start_idx:stop_idx]
                option_date = request.form.get(f"option{option_id}_date", None)
                option_start = request.form.get(f"option{option_id}_start", None)
                option_end = request.form.get(f"option{option_id}_end", None)
                new_label = f"{option_date}T{option_start} - {option_date}T{option_end}"
                choice = queries.get_choice_by_id(option_id)
                queries.update_choice(option_id, label=new_label)
                choice = queries.get_choice_by_id(option_id)
            else:
                if m2:
                    start_idx, stop_idx = m2.span()
                    option_id = option[0][7:][start_idx:stop_idx]
                    option_date = request.form.get(f"optionn{option_id}_date", None)
                    option_start = request.form.get(f"optionn{option_id}_start", None)
                    option_end = request.form.get(f"optionn{option_id}_end", None)
                    new_label = f"{option_date}T{option_start} - {option_date}T{option_end}"
                    poll = queries.get_poll_by_appointment_id(appointment.id)
                    poll_id = None
                    if not poll:
                        poll_id = queries.create_poll(appointment.id, "")
                    else:
                        poll_id = poll.id
                    queries.create_choice(poll_id, label=new_label)

    return redirect(url_for("get_appointment", user_id=user.id, appointment_id=appointment.id))

@app.post("/users/<user_id>/appointments/<appointment_id>/date-fix")
def date_fix(user_id, appointment_id):
    user = queries.get_user_by_id(user_id)
    appointment = queries.get_appointment_by_id(appointment_id)
    if not user or not appointment:
        redirect(url_for("index"))
    final_choice_id = request.form.get("final_choice_id", None)
    if final_choice_id:
        choice = queries.get_choice_by_id(final_choice_id)
        start_datetime = datetime.fromisoformat(choice.label.split(" - ")[0])
        end_datetime = datetime.fromisoformat(choice.label.split(" - ")[1])
        queries.update_appointment(appointment.id, start_datetime=start_datetime,
                                   end_datetime=end_datetime)
        return redirect(url_for("user_home", user_id=user.id))
if __name__ == '__main__':
    app.run(debug=True)
