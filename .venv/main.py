from flask import Flask, redirect
import doodle
import queries

app = flask.Flask(__name__)

app.route('/appointments/<appointment_id>', methods=['GET'])

app.route('appointments/<appointment_id>/create_doodle', methods=['POST'])
def create_doodle(appointment_id):
    poll_description = request.form['poll_description']
    poll = queries.create_poll(appointment_id, poll_description)
    doodle_dates = request.form["dates"]
    for dateentry in doodle_dates.split(","):
        queries.create_choice(poll.id, dateentry)
    return redirect(url_for("appointments", appointments=appointment(id)))

if __name__ == '__main__':
    app.run(debug=True)
