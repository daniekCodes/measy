from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)



# Routing for home
@app.route("/")
def main():
    return render_template("index.html")

# Routing for Create Event page
@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    # when clicking save
    if request.method == "POST":
        return redirect(url_for("main"))
    return render_template("create_event.html")


@app.route("/event_details")
def event_details():
    event = {
        "id": 1,
        "title": "Test titel",
        "description": "test description",
        "location_type": "physical",
        "street": "vvv",
        "housenumber": "1",
        "plz": "12345",
        "city": "vvv"
    }

    choices = [
        {"id": 1, "label": "Freitag, 20:00"},
        {"id": 2, "label": "Samstag, 19:00"},
        {"id": 3, "label": "Samstag, 18:00"}
    ]

    return render_template(
            "event_details.html", event=event, choices=choices
        )

if __name__ == "__main__":
    app.run(debug=True)  # server restarts when making changes