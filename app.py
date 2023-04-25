from flask import Flask
from views import *

app = Flask(__name__)

# register blueprints
app.register_blueprint(expenses)

# Set a secret key for flash messages
app.secret_key = 'your_secret_key'


if __name__ == '__main__':
    create_table_database()

    app.run()

