import schedule
import time
import worker

# Schedule for Midnight US Central Time
schedule.every().day.at("01:00:00").do(worker.main)

while True:
    schedule.run_pending()
    time.sleep(1)
