import os
from dotenv import load_dotenv

load_dotenv()

login = os.getenv('EMAIL_LOGIN')
senha = os.getenv('EMAIL_PASSWORD')
email_receiver = os.getenv('EMAIL_RECEIVER')
