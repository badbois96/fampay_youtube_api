### Assignment Description
To make an API to fetch latest videos sorted in reverse chronological order of their 
publishing date-time from YouTube for a given tag/search query in a paginated response.

## API Description
 - To get all videos: http://localhost:8000/getvideos/?q=&page=1
 - To search with a query along with pagination: http://localhost:8000/getvideos/?q=mika%20singh&page=1
 <br><br>
 <b>Note:</b> By default I'm only fetching music videos from www.youtube.com in every 5 minutes. 
   But you can change that by replacing the `'search_query': <your_tag>` at line 119 in settings.py
   before firing the <b>Docker</b>
   
## Docker Instructions
#### Backend
 - Append your API_KEY to keys.json file which you obtained 
 from https://console.developers.google.com/apis/api/youtube.googleapis.com/ 
 - `docker build -t fampay .`
 - `docker run -it -d -p 8000:80 fampay` Print container ID
 - `docker exec -it <-put container ID here-> /bin/sh` Get interactive shell to container 
 - `python manage.py qcluster` Starts django-Q cluster 
#### Frontend
 - Open new terminal/CMD 
 - `cd ./frontend`
 - `docker build -t frontend .`
 - `docker run -it -d -p 3000:80 frontend`
 - Visit http://localhost:3000/ 
## Development
### How to <i>Setup</i>
 - Install Python 3.x from https://www.python.org/downloads
 - `pip install pipenv`
 - `pipenv shell`
 - `pipenv install`
 - `python manage.py makemigrations`
 - `python manage.py createcachetable`
 - `python manage.py migrate`
 - `python manage.py startservice`
 - Install LTS version of Node from https://nodejs.org/en/
 - `cd frontend/`
 - `npm i`
 
### How to <i>Configure</i>
#### Django
 - `cd fampay`
 - `touch settings.py`
 - Line 119: add your search query for which the job will insert entries in database
 - Append your API_KEY to keys.json file which you obtained 
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
