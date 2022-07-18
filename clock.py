import schedule
import time
import worker

# Schedule for Midnight GMT
schedule.every().day.at("04:01:00").do(worker.main)

while True:
    schedule.run_pending()
    time.sleep(1)
