import schedule
import time
import worker

schedule.every().day.at("21:50:00").do(worker.main)

while True:
    schedule.run_pending()
    time.sleep(1)
