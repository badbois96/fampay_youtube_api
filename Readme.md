### Assignment Description
To make an API to fetch latest videos sorted in reverse chronological order of their 
publishing date-time from YouTube for a given tag/search query in a paginated response.

### How to <i>Setup</i>
 - Install Python 3.x from https://www.python.org/downloads
 - `pip install pipenv`
 - `pipenv shell`
 - `pipenv install`
 - `python manage.py makemigrations`
 - `python manage.py createcachetable`
 - `python manage.py migrate`
 - Install LTS version of Node from https://nodejs.org/en/
 - `cd frontend/`
 - `npm i`
 
### How to <i>Configure</i>
#### Django
 - `cd fampay`
 - `touch settings.py`
 - Line 119: add your domain
 - Line 121: add your api_keys which you got 
 from https://console.developers.google.com/apis/api/youtube.googleapis.com/ 
#### Node
 - `cd frontend`
 - `npm run build`

### How to <i>RUN</i>
#### Django-Q
 - `pepenv shell` 
 - `python manage.py qcluster`
#### Django
 - `pepenv shell` 
 - `python manage.py runserver`
 - Go to http://127.0.0.1:8000/