import pandas as pd
from config import Config

class DBHandler:
    def __init__(self):
        self.database_file = Config.DATABASE_FILE

    def authenticate_user(self, mobile, otp):
        df = pd.read_excel(self.database_file)
        user_data = df[(df['Mobile'] == mobile) & (df['OTP'] == otp)].to_dict('records')
        return user_data[0] if user_data else None

    def save_user_data(self, user_data):
        df = pd.read_excel(self.database_file)
        df = df.append(user_data, ignore_index=True)
        df.to_excel(self.database_file, index=False)
