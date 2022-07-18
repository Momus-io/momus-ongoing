import sched
from apscheduler.schedulers.blocking import BlockingScheduler
import worker

scheduler = BlockingScheduler()

scheduler.add_job(worker.main(), "cron", hour=21, minute=33)

scheduler.start()
