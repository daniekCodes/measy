from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # mock data
    mock_events = [
        {"title": "Frontend Review", "start": "2026-03-12"},
        {"title": "Database Update", "start": "2026-03-15"}
    ]

    # return to backend
    return render_template('index.html', events_data=mock_events)


if __name__ == '__main__':
    app.run(debug=True)