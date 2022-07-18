import schedule
import time
import worker

# Schedule for Midnight GMT
schedule.every(3).minutes.do(worker.main)

while True:
    schedule.run_pending()
    time.sleep(1)
