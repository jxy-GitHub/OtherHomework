import os

STATE = False

user_dict = {"user_name": None, "card_number": None, "password": None, "balance": 0, "login_date": None}

BASE_PATH = os.path.dirname(os.getcwd())
user_path = os.path.join(BASE_PATH, 'db')
log_path = os.path.join(BASE_PATH, 'log')
