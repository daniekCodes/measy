from datetime import datetime
from flask import Flask, redirect, render_template, request, jsonify, url_for
import queries
from dataclasses import dataclass


@dataclass
class DoodleVote:
    date: datetime
    count_votes: int


app = Flask(__name__)
app.url_map.strict_slashes = False

# --- MOCK DATABASE (SINGLE SOURCE OF TRUTH) ---
MOCK_DB = {
    "1": {
        "id": 1,
        "title": "Leeres Event",
        "start_datetime": "Noch nicht festgelegt",
        "description": "Leer",
        "date_start": None,
        "options": []
    },
    "2": {
        "id": 2,
        "title": "Doodle",
        "start_datetime": "Abstimmung ausstehend",
        "description": "Bitte stimme ab",
        "date_start": None,
        "options": [
            {"id": 101, "date": "01.05.2026, 13:00"},
            {"id": 102, "date": "15.05.2026, 12:00"},
            {"id": 103, "date": "21.05.2026, 13:30"}
        ]
    },
    "3": {
        "id": 3,
        "title": "Festes Datum beispiel",
        "start_datetime": "25.03.2026 14:00",
        "description": "Dieses Event hat ein festes Datum.",
        "date_start": datetime(2026, 3, 25, 14, 0),
        "options": []
    },
    "4": {
        "id": 4,
        "title": "Festes Datum beispiel 2",
        "start_datetime": "15.12.2026 18:00",
        "description": "Dieses Event hat ein festes Datum.",
        "date_start": datetime(2026, 12, 15, 18, 0),
        "options": []
    }
}


@app.route("/")
def home():
    return render_template("index.html")


# --- LOGIN ROUTE (MOCKED) ---
@app.route("/users", methods=["POST"])
def create_user():
    return redirect(url_for("user_home", user_id=1))


# --- DASHBOARD ROUTE ---
@app.route("/users/<user_id>", methods=["GET"])
def user_home(user_id):
    dummy_user = {"id": user_id, "name": "Daniek"}

    # Pulls directly from the mock database above
    dummy_events = [MOCK_DB["1"], MOCK_DB["2"]]
    dummy_invitations = [MOCK_DB["3"], MOCK_DB["4"]]

    return render_template(
        "home.html",
        user=dummy_user,
        events=dummy_events,
        invitations=dummy_invitations
    )


# --- APPOINTMENT LOGIC ---
@app.route("/users/<user_id>/appointments", methods=["POST"])
def create_appointment(user_id):
    title = request.form["title"]
    description = request.form["description"]
    date_start = datetime.now()
    queries.create_appointment(title, int(user_id), 1, description, date_start)
    return redirect(url_for("user_home", user_id=user_id))


@app.route('/users/<user_id>/appointments/create', methods=['GET'])
def new_appointment(user_id):
    return render_template("create_event.html", user_id=user_id)


# 1. DETAILS/VOTING PAGE
@app.route('/users/<user_id>/appointments/<appointment_id>', methods=['GET'])
def get_appointment(user_id, appointment_id):
    # .get() grabs the event from MOCK_DB, or defaults to event "1" if not found
    mock_event = MOCK_DB.get(str(appointment_id), MOCK_DB["1"])
    mock_options = mock_event["options"]

    return render_template("event_details.html", event=mock_event, options=mock_options, user_id=user_id)


# 2. EDIT PAGE
@app.route('/users/<user_id>/appointments/<appointment_id>/edit', methods=['GET'])
def edit_appointment(user_id, appointment_id):
    # Grabs the exact same event data for the edit page
    mock_event = MOCK_DB.get(str(appointment_id), MOCK_DB["1"])
    return render_template("edit_event.html", event=mock_event, user_id=user_id)


# 3. VOTING SUBMISSION
@app.route('/users/<user_id>/appointments/<appointment_id>/vote', methods=['POST'])
def create_vote(user_id, appointment_id):
    return redirect(url_for("user_home", user_id=user_id))


# --- OTHER ROUTES ---
@app.route("/appointments/showall", methods=["GET"])
def show_all_appointments():
    appointments = queries.get_all_appointments()
    return jsonify(appointments)


@app.route('/users/<user_id>/appointments/<appointment_id>/create_doodle', methods=['POST'])
def create_doodle(appointment_id):
    poll_description = "test poll"
    poll = queries.create_poll(appointment_id, poll_description)
    doodle_dates = [request.form["date1"], request.form["date2"], request.form["date3"]]
    for doodle_date in doodle_dates:
        queries.create_choice(poll.id, doodle_date)
    return redirect(url_for("get_appointment", user_id=1, appointment_id=appointment_id))


if __name__ == '__main__':
    app.run(debug=True)