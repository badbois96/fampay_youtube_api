from django.core.management.base import BaseCommand, CommandError
from django_q.models import Schedule
from django.conf import settings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(module)s [%(levelname)s] %(message)s')


class Command(BaseCommand):
    help = "Instantiated the youtube backround job"

    def handle(self, *args, **options):
        job_name = settings.YT_BACKGROUND_JOB['name']
        func = settings.YT_BACKGROUND_JOB['func_name']

        if Schedule.objects.filter(name=job_name).count() == 0:
            '''
            Checking if the same job is already exists and running in Django-Q cluster
            If not then create a new record with an interval value of 5 minutes (default)

            https://django-q.readthedocs.io/en/latest/schedules.html
            '''

            Schedule.objects.create(
                name=job_name,
                func=func,
                minutes=5,
                schedule_type=Schedule.MINUTES,
            )
            logging.info('%s Job scheduled', job_name)
        else:
            logging.info('Entry for %s already exists in django_q_schedule', job_name)
