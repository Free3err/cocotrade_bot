import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .instance.db.handlers import FarmHandler

scheduler = BackgroundScheduler()


def update_all_farms_job():
    try:
        updated_farms = FarmHandler.update_all_farms()
        logging.info(f"Successfully updated {updated_farms} farms")
    except Exception as e:
        logging.error(f"Error while updating farms: {str(e)}")


def start():
    if not scheduler.running:
        scheduler.add_job(
            update_all_farms_job,
            IntervalTrigger(hours=1),
            id='update_farms_job',
            name='Updating all farms',
            replace_existing=True
        )

        scheduler.start()
        logging.info("Scheduler has started!")