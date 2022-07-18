import schedule
import time
import worker

schedule.every().day.at("22:09").do(worker.main)

while True:
    schedule.run_pending()
    time.sleep(1)
