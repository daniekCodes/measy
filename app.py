from flask import Flask, render_template

app = Flask(__name__)


# This tells the server: "When someone visits the home URL (/), run this function"
@app.route('/')
def home():
    # This simulates the data your backend developer will eventually send you!
    mock_events = [
        {"title": "Frontend Review", "start": "2026-03-12"},
        {"title": "Database Update", "start": "2026-03-15"}
    ]

    # This tells Flask to process your Jinja template and pass the data to it
    return render_template('index.html', events_data=mock_events)


if __name__ == '__main__':
    app.run(debug=True)