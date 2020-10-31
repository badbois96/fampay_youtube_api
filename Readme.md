#### Steps to <i>Setup</i>
 - Install Python 3.x from https://www.python.org/downloads
 - `pip install pipenv`
 - `pipenv install`
 - `python manage.py createcachetable`
 - `python manage.py migrate`
 - Install LTS version of Node
 - `cd frontend/`
 - `npm i`
 - `npm run build`

#### Steps to <i>RUN</i>
 - `python manage.py qcluster`
 - `python manage.py runserver`
 
#### Project Description
To make an API to fetch latest videos sorted in reverse chronological order of their 
publishing date-time from YouTube for a given tag/search query in a paginated response.