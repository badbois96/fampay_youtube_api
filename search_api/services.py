from search_api.models import Youtube
import logging
from django.conf import settings
import requests
from requests.models import Response
from datetime import datetime, timezone, timedelta
import os
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(module)s [%(levelname)s] %(message)s')


def background_update():
    '''
    Main background job for updating Youtube table with new records
    Note: By default this job run at an interval of updates in 5 minutes and queries all the new videos uploaded
    to youtube.com in last 5 minutes
    :return: None
    '''

    search_query = settings.YT_BACKGROUND_JOB['search_query']
    developer_keys_path = os.path.join(settings.BASE_DIR, 'keys.json')

    with open(developer_keys_path, 'rb') as keys_file:
        DEVELOPER_KEYS_OBJECT = json.load(keys_file)
        DEVELOPER_KEYS = DEVELOPER_KEYS_OBJECT["yt_api_keys"]

    part = "snippet"
    maxResults = 50
    order = "date"
    publishedAfter = get_past_five_mins_timestamp()
    count = 0

    try:
        '''
        Support for supplying multiple API keys so that if quota is exhausted on one, new API_KEY will be picked up
         automatically from the list of API Keys provided in settings.py
        '''
        for developer_key in DEVELOPER_KEYS:
            response = fetch_data(developer_key=developer_key,
                                  part=part,
                                  maxResults=maxResults,
                                  search_query=search_query,
                                  order=order,
                                  publishedAfter=publishedAfter)

            if response.status_code == 400:
                '''
                if request results in 400, then new API_KEY will be picked up
                '''
                logging.warning(f"{developer_key} Expired.")
                continue

            if response.status_code == 200:
                '''
                If status is 200 then new entries are made in Youtube table
                '''
                logging.debug(response.status_code)
                count = 0
                for item in response.json()["items"]:
                    try:
                        Youtube(
                            title=item["snippet"]["title"],
                            description=item["snippet"]["description"],
                            published_at=item["snippet"]["publishedAt"],
                            thumbnail_url=item["snippet"]["thumbnails"]["default"]["url"],
                            video_id=item["id"]["videoId"],
                            channel_title=item["snippet"]["channelTitle"],
                            channel_id=item["snippet"]["channelId"],
                        ).save()
                        count += 1
                    except Exception as e:
                        '''
                        Only unique entries will be saved.
                        Uniqueness is identified using video_id from youtube.com
                        '''
                        # logging.warning(e)
                        continue
                break

    except Exception as e:
        logging.error(e)

    logging.info(f"Database updated with {count} new entries of {search_query}")


def fetch_data(developer_key: str, part: str, order: str, search_query: str, maxResults: int,
               publishedAfter: str) -> Response:
    url = f"https://youtube.googleapis.com/youtube/v3/search?" \
          f"part={part}&" \
          f"maxResults={maxResults}&" \
          f"order={order}&" \
          f"publishedAfter={publishedAfter}&" \
          f"q={search_query}&" \
          f"key={developer_key}"

    return requests.get(url=url)


def get_past_five_mins_timestamp():
    utc_past_hour = datetime.utcnow() + timedelta(minutes=-5)
    my_time = str(utc_past_hour.replace(tzinfo=timezone.utc)).split(' ')
    return f"{my_time[0]}T{my_time[1][:-6]}Z"


def dummy():
    print('Scheduled Task')
