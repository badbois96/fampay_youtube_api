from django.http import JsonResponse
from django_q.models import Schedule
from django_q.tasks import async_task
import logging
from django.core.paginator import Paginator
from search_api.models import Youtube
from search_api.serializers import YoutubeSerializer

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(module)s [%(levelname)s] %(message)s')


def index(request):
    json_payload = {"message": "hello world!"}

    # async_task("search_api.services.yt_search.background_job")
    # async_task("search_api.services.background_update")

    # Schedule.objects.create(
    #     name='dummy_job',
    #     func="search_api.services.dummy",
    #     schedule_type=Schedule.MINUTES,
    # )

    # import search_api.services as my_service
    #
    # my_service.background_update()

    return JsonResponse(json_payload)


''' 
    getvideos/?q=messi&page=1
'''


def get_videos(request):
    query_title = request.GET.get('q')
    query_desc = request.GET.get('desc')
    page_number = int(request.GET.get('page'))

    query_title_string = ""
    if query_title is not None and len(query_title) > 0:
        query_title_string = "and ("
        for item in query_title.split(' '):
            query_title_string += f" title like '%{item}%' or"

        query_title_string = query_title_string[:-3] + ")"

    query_desc_string = ""
    if query_desc is not None and len(query_desc) > 0:
        query_desc_string = "and ("
        for item in query_desc.split(' '):
            query_desc_string += f" description like '%{item}%' or"

        query_desc_string = query_desc_string[:-3] + ")"

    final_query = r"""SELECT * from search_api_youtube where 1=1 %s %s"""

    try:
        # search_results = Youtube.objects.raw(final_query, [query_title_string, query_desc_string])
        search_results = Youtube.objects.filter(title__icontains=query_title if query_title is not None else ''
                                                , description__contains=query_desc if query_desc is not None else '')\
            .order_by('-published_at')

        paginator = Paginator(search_results, 25)
        page_obj = paginator.get_page(page_number)

        serialized_results = YoutubeSerializer(page_obj.object_list, many=True)

        return JsonResponse({"result": serialized_results.data})
    except Exception as e:
        logging.error(e)
        return JsonResponse({"success": "failed", "result": e})
