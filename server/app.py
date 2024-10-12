from flask import Flask, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, Author, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return 'Validations lab'

@app.errorhandler(404)
def not_found(error):
    return make_response({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return make_response({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure all tables are created
    app.run(port=5555, debug=True)
