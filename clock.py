import schedule
import time
import worker

# Schedule for Midnight GMT
schedule.every(24).hours.do(worker.main)

while True:
    schedule.run_pending()
    time.sleep(1)
