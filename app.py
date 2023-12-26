# app.py
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from db_handler import DBHandler
from otp_handler import OTPHandler
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
db_handler = DBHandler()
otp_handler = OTPHandler()

@app.route('/send_otp', methods=['POST'])
def send_otp_route():
    try:
        data = request.get_json()
        mobile = data['mobile']

        # Generate a random OTP (for demo purposes; replace with a secure method)
        otp = '123456'

        # Send OTP to the user's mobile using 2Factor
        response = otp_handler.send_otp(mobile, otp)

        if response['Status'] == 'Success':
            return jsonify({'message': 'OTP sent successfully'}), 200
        else:
            return jsonify({'error': 'Failed to send OTP'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        mobile = data['mobile']
        otp = data['otp']

        # Verify the OTP
        if not otp_handler.verify_otp(mobile, otp):
            return jsonify({'error': 'Invalid OTP'}), 401

        # Authenticate the user
        user_data = db_handler.authenticate_user(mobile, otp)

        if not user_data:
            # Save user data if not already present
            db_handler.save_user_data({'Mobile': mobile, 'OTP': otp})

        # Create and return JWT token
        access_token = create_access_token(identity=mobile)
        return jsonify(access_token=access_token), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        mobile = data['mobile']
        otp = data['otp']

        # Verify the OTP
        if not otp_handler.verify_otp(mobile, otp):
            return jsonify({'error': 'Invalid OTP'}), 401

        # Authenticate the user
        user_data = db_handler.authenticate_user(mobile, otp)

        if not user_data:
            return jsonify({'error': 'Invalid credentials'}), 401

        # Create and return JWT token
        access_token = create_access_token(identity=mobile)
        return jsonify(access_token=access_token), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
