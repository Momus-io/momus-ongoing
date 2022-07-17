from apscheduler.schedulers.background import BlockingScheduler
import worker

sched = BlockingScheduler()


@sched.scheduled_job("cron", hour=12, minute=12)
def scheduled_job():
    worker.main()


sched.start()
