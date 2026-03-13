from flask import Flask, redirect, render_template, request, jsonify
import doodle
import queries
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/appointments", methods=["POST", "GET"])
def create_appointments():
    #title = request.form["title"]
    queries.create_appointment("title", 1, 1)
    appointments = []
    for appointment in queries.get_all_appointments():
        appointments.append(appointment.id)
    return render_template("create_event.html")

@app.route("/appointments/showall", methods=["GET"])
def show_all_appointments():
    appointments = []
    for appointment in queries.get_all_appointments():
        appointment_dic = {
            "id": appointment.id,
            "title": appointment.title,
            "date": appointment.start_datetime
        }
        #appointment_data = json.dumps(appointment, default=lambda o: o.__dict__, indent=4)
        appointments.append(appointment)
    return jsonify(appointments)

@app.route('/appointments/<appointment_id>', methods=['POST', 'GET'])
def get_appointment(appointment_id):
    #if request.method == "POST":

    return str(queries.get_appointment_by_id(appointment_id).id)

@app.route('/appointments/<appointment_id>/create_doodle', methods=['POST'])
def create_doodle(appointment_id):
    poll_description = "test poll"   # request.form["poll_description"]
    poll = queries.create_poll(appointment_id, poll_description)
    doodle_date = "22.2.2022"   # request.form["dates"]
    queries.create_choice(poll.id, doodle_date)
    choices = []
    for choice in Session(engine).query(Choice).all():
        choices.append(choice.label)
    return redirect("/appointments/<appointment_id>/show_doodle", code=302)

@app.route('/appointments/<appointment_id>/show_doodle', methods=['GET'])
def show_doodle(appointment_id):
    choices = []
    for choice in Session(engine).query(Choice).all():
        choices.append(choice.label)
    return choices

if __name__ == '__main__':
    app.run(debug=True)
