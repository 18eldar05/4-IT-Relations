from relations.celery import app
from .service import send
import schedule
import time


@app.task
def send_notification():
    send()
    schedule.every().day.at("07:55").do(send)
    while True:
        schedule.run_pending()
        time.sleep(1)
