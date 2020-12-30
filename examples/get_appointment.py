import os
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from dikidi import DikidiAPI


def get_appointment():
    date_object = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1),
                                            datetime.time.min).strftime('%Y-%m-%d')
    api = DikidiAPI(os.environ.get('LOGIN_DIKIDI'), os.environ.get('PASSWORD_DIKIDI'))
    appointment_list = api.get_appointment_list(os.environ.get('COMPANY_DIKIDI'), date_object, date_object, limit=50)
    print(appointment_list)


if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone='Europe/Moscow')
    scheduler.add_job(get_appointment, CronTrigger.from_crontab(os.environ.get('CRON_EXPRESSION')))
    scheduler.start()
