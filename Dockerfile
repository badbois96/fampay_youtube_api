FROM python:3.8.6-alpine3.12 as pyt

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
ADD ./requirements.txt .

RUN pip install -r requirements.txt
ADD . .
RUN python manage.py makemigrations \ 
    && python manage.py createcachetable \
    && python manage.py migrate \
    && python manage.py startservice

EXPOSE 80

CMD gunicorn fampay.wsgi:application --bind 0.0.0.0:80
