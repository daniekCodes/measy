from flask import Flask
app = flask.Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)
