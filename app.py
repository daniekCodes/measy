from flask import Flask, render_template

app = Flask(__name__)



# Routing for home
@app.route("/")
def home():
    return render_template(
        "index.html",
        events=[], # for events fetch
        invitations=[], # for invitations fetch
        polls=[] # for polls fetch
    )

# Routing for Create Event page
@app.route("/create_event")
def create_event():
    return render_template("create_event.html")

if __name__ == "__main__":
    app.run(debug=True) # server restarts when making changes