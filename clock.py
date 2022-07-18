import schedule
import time
import worker

schedule.every().day.at("22:13").do(worker.main)
print("RUNNING")
while True:
    schedule.run_pending()
    time.sleep(1)
