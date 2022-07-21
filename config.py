import os
from dotenv import load_dotenv

load_dotenv(".env")

env_vars = {
    "authorization": os.getenv("AUTHORIZATION"),
    "db_name": os.getenv("DB_NAME"),
    "db_user": os.getenv("DB_USER"),
    "db_pass": os.getenv("DB_PASS"),
    "db_host": os.getenv("DB_HOST"),
    "db_port": os.getenv("DB_PORT"),
    "twilio_sid": os.getenv("TWILIO_SID"),
    "twilio_token": os.getenv("TWILIO_TOKEN"),
    "twilio_to": os.getenv("TWILIO_TO"),
    "twilio_from": os.getenv("TWILIO_FROM")
}
