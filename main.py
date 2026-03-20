from datetime import datetime
from flask import Flask, redirect, render_template, request, jsonify, url_for

app = Flask(__name__)
app.url_map.strict_slashes = False

# --- MOCK DATABASE (Fully Synced with Chris) ---
# Each entry now contains the exact keys Chris specified
MOCK_DB = {
    "1": {
        "appointment": {
            "id": 1,
            "title": "Leeres Event",
            "description": "Dieses Event hat noch keine Termine.",
            "organizer": "Test User",
            "date_start": None # Chris's date field
        },
        "location": "Büro A, Etage 2",
        "poll": None,
        "choices": [],
        "attendance_status": None,
        "votes": 0
    },
    "2": {
        "appointment": {
            "id": 2,
            "title": "Doodle",
            "description": "Bitte stimme für die gewünschten Termine ab.",
            "organizer": "Gerald von Rivia",
            "date_start": None
        },
        "location": "Hauptstraße 1, 12345 Berlin",
        "poll": True,
        "choices": [
            {"id": 101, "date": "01.05.2026, 13:00", "votes": 3},
            {"id": 102, "date": "15.05.2026, 12:00", "votes": 1},
            {"id": 103, "date": "21.05.2026, 13:30", "votes": 4}
        ],
        "attendance_status": None,
        "votes": 8
    },
    "3": {
        "appointment": {
            "id": 3,
            "title": "Festes Datum Beispiel",
            "description": "Dieses Event hat ein festes Datum.",
            "organizer": "Christopher Wollny",
            "date_start": datetime(2026, 3, 25, 14, 0)
        },
        "location": "Konferenzraum Blau",
        "poll": None,
        "choices": [],
        "attendance_status": "Nehme teil",
        "votes": 0
    }
}

@app.route("/")
def home():
    return render_template("index.html")
# --- LOGIN ROUTE (Needed for index.html) ---
@app.route("/users", methods=["POST"])
def create_user():
    """Handles the login form from index.html and redirects to the dashboard."""
    # For the mockup, we just redirect everyone to User 1 (Daniek)
    return redirect(url_for("user_home", user_id=1))

# --- DASHBOARD ---
@app.route("/users/<user_id>", methods=["GET"])
def user_home(user_id):
    dummy_user = {"id": user_id, "name": "Daniek"}
    # We pass the full data objects so home.html can find appointment.date_start
    events_list = [v for v in MOCK_DB.values()]
    return render_template("home.html", user=dummy_user, events=events_list, invitations=[])

# --- DETAILS PAGE ---
@app.route('/users/<user_id>/appointments/<appointment_id>', methods=['GET'])
def get_appointment(user_id, appointment_id):
    data = MOCK_DB.get(str(appointment_id), MOCK_DB["1"])
    # Unpacking the data for the template
    return render_template(
        "event_details.html",
        user_id=user_id,
        appointment=data["appointment"],
        location=data["location"],
        poll=data["poll"],
        choices=data["choices"],
        attendance_status=data["attendance_status"],
        votes=data["votes"]
    )

# --- DATE FIX ---
@app.route('/users/<user_id>/appointments/<appointment_id>/date_fix', methods=['GET'])
def date_fix(user_id, appointment_id):
    data = MOCK_DB.get(str(appointment_id), MOCK_DB["2"])
    return render_template(
        "date_fix.html",
        user_id=user_id,
        appointment=data["appointment"],
        choices=data["choices"],
        total_votes=data["votes"],
        total_invited=5
    )


@app.route('/users/<user_id>/appointments/create', methods=['GET'])
def new_appointment(user_id):
    return render_template("create_event.html", user_id=user_id)
@app.route("/users/<user_id>/appointments", methods=["POST"])
def create_appointment(user_id):
    """Handles the form submission from create_event.html"""
    # In a real app, Chris would save the form data to the database here.
    # For now, we just redirect you back to the dashboard.
    return redirect(url_for("user_home", user_id=user_id))

@app.route('/users/<user_id>/appointments/<appointment_id>/edit', methods=['GET'])
def edit_appointment(user_id, appointment_id):
    data = MOCK_DB.get(str(appointment_id), MOCK_DB["1"])
    return render_template("edit_event.html", event=data["appointment"], user_id=user_id)

@app.route('/users/<user_id>/appointments/<appointment_id>/vote', methods=['POST'])
def create_vote(user_id, appointment_id):
    return redirect(url_for("user_home", user_id=user_id))

@app.route('/users/<user_id>/appointments/<appointment_id>/set_date', methods=['POST'])
def set_fixed_date(user_id, appointment_id):
    return redirect(url_for("get_appointment", user_id=user_id, appointment_id=appointment_id))

if __name__ == '__main__':
    app.run(debug=True)