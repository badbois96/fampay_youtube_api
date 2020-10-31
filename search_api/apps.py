from django.apps import AppConfig
from django.conf import settings
import logging

logging.basicConfig(level=logging.NOTSET, format='%(asctime)s %(module)s [%(levelname)s] %(message)s')


class SearchApiConfig(AppConfig):
    name = 'search_api'

    def ready(self):
        try:
            from django_q.models import Schedule

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

        except ImportError as e:
            logging.error(e)
