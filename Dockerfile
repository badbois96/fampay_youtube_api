FROM python:3.8.6-alpine3.12 as pyt

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD ./search_api search_api

ADD ./fampay fampay

ADD ./manage.py manage.py

ADD ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN python manage.py makemigrations

RUN python manage.py createcachetable

RUN python manage.py migrate

ADD ./frontend/build /app/frontend/build

FROM nginx

RUN rm -rf /usr/share/nginx/html/*

COPY --from=pyt /app/frontend/build /usr/share/nginx/html/

ADD nginx.conf /etc/nginx/nginx.conf

EXPOSE 80 80

CMD ["nginx", "-g", "daemon off;"]
