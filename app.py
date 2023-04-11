from flask import Flask
from views import *

app = Flask(__name__)

# register blueprints
app.register_blueprint(expenses)

if __name__ == '__main__':
    create_table_database()
    app.run()

