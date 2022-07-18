from apscheduler.schedulers.background import BlockingScheduler
import worker

sched = BlockingScheduler()


@sched.scheduled_job("cron", hour=20, minute=2)
def scheduled_job():
    worker.main()


sched.start()
