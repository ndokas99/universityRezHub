from flask import Flask, render_template, redirect, request, session, flash, \
    make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from os import path


app = Flask(__name__)
settings = {
    "SECRET_KEY": 'AADHI43JJ5J5JJ7K5',
    "SQLALCHEMY_DATABASE_URI": 'sqlite:///database.db',
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
}
app.config.update(settings)
app.debug = True
db = SQLAlchemy(app)


class Universities(db.Model):
    uniId = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    location = db.Column(db.Text, unique=True, nullable=False)
    phone = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    img = db.Column(db.Text, unique=True, nullable=False)


class Residence(db.Model):
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    universityID = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, unique=False, nullable=False)
    address = db.Column(db.Text, unique=False, nullable=False)
    contact = db.Column(db.Text, unique=False, nullable=False)


@app.route('/')
def index():
    uni = Universities.query.filter_by(uniId="nust").first()
    res = Residence.query.filter_by(universityID=uni.uniId).all()
    hostels = []
    j = -1
    for i in range(len(res)):
        if i % 3 == 0:
            hostels.append([])
            j += 1
        hostels[j].append(res[i])
    return render_template('index.html', university=uni, residence=hostels)


def create_database():
    if not path.exists("/instance/database.db"):
        try:
            db.create_all()
        except IntegrityError:
            pass
        except OperationalError:
            pass


if __name__ == '__main__':
    with app.app_context():
        create_database()
        app.run('0.0.0.0')
