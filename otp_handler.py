import requests
from config import Config

class OTPHandler:
    def __init__(self):
        self.api_key = Config.TWO_FACTOR_API_KEY

    def send_otp(self, mobile, otp):
        url = f'https://2factor.in/API/V1/{self.api_key}/SMS/{mobile}/{otp}'
        response = requests.get(url)
        return response.json()

    def verify_otp(self, mobile, otp):
        # Add your own OTP verification logic here
        # For simplicity, let's assume the OTP is valid if it matches '123456'
        return otp == '123456'
