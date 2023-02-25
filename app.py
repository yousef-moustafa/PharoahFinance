from flask import Flask, render_template
from views import *

app = Flask(__name__)

# register blueprints
app.register_blueprint(expenses)

if __name__ == '__main__':
    app.run()
