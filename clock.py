from apscheduler.schedulers.background import BlockingScheduler
import worker

sched = BlockingScheduler()


@sched.scheduled_job("cron", hour=19, minute=52)
def scheduled_job():
    worker.main()


sched.start()
