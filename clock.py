from apscheduler.schedulers.background import BlockingScheduler
import worker

sched = BlockingScheduler()


@sched.scheduled_job("cron", hour=0, minute=1)
def scheduled_job():
    worker.main()


sched.start()
