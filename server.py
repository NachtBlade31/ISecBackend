from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask_security.utils import hash_password
from flask_cors import CORS
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///society.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['SECURITY_PASSWORD_SALT'] = 'super-secret-salt'
CORS(app)

db = SQLAlchemy(app)

# Define models for User, Role, and Flat
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    mobile_number = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)
    otp = db.Column(db.String(6), nullable=True)
    flat_number = db.Column(db.String(10), nullable=True)

class Flat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flat_number = db.Column(db.String(10), unique=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tenants = db.relationship('User', secondary='flat_tenants', backref=db.backref('flats', lazy='dynamic'))

class FlatTenants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flat_id = db.Column(db.Integer, db.ForeignKey('flat.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, RoleMixin)
security = Security(app, user_datastore)

# Routes
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    mobile_number = data.get('mobile_number')
    
    # Generate OTP
    otp = str(random.randint(100000, 999999))

    # Save OTP to the user in-memory data structure
    user = User(mobile_number=mobile_number, otp=otp)
    db.session.add(user)
    db.session.commit()

    # TODO: Send OTP to the user's mobile number (You can use a third-party service or a mobile gateway for this)

    return jsonify({'message': 'OTP sent successfully'})

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    mobile_number = data.get('mobile_number')
    otp_entered = data.get('otp')

    user = User.query.filter_by(mobile_number=mobile_number, otp=otp_entered).first()

    if user:
        # OTP is valid, remove it from the user record
        user.otp = None
        db.session.commit()

        return jsonify({'message': 'OTP verified successfully'})
    else:
        return jsonify({'error': 'Invalid OTP'}), 401

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
