"""
Entrypoint for the flask app
Launches the app in a standalone window
"""

from flask import Flask
from webui import WebUI

# launch our flask app
app = Flask(__name__)
# launch our app's window
ui = WebUI(app, debug=True)


@app.route("/")
def hello():
    "say hello"
    return "Hello World !"

if __name__ == '__main__':
    ui.run()
