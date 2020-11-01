from django.http import JsonResponse, HttpResponse
import logging
from django.core.paginator import Paginator
from search_api.models import Youtube
from search_api.serializers import YoutubeSerializer
import os
from django.conf import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(module)s [%(levelname)s] %(message)s')


def web_page(request):
    '''
    Serving index.html
    :param request:
    :return:
    '''

    try:
        with open(os.path.join(settings.REACT_APP_DIR, 'build', 'index.html')) as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        logging.exception('Production build of app not found')
        return HttpResponse(
            """
            Contact with Admin.
            """,
            status=404,
        )


def index(request):
    '''
     Demo API for testing
    :param request:
    :return:
    '''


    json_payload = {"message": "hello world!"}

    return JsonResponse(json_payload)


def get_videos(request):
    '''
    A GET API which returns the stored video data in a paginated response sorted in descending order of published
    datetime.
    getvideos/?q=messi&page=1

    :param request:
    :return:
    '''

    query_title = request.GET.get('q')
    query_desc = request.GET.get('desc')
    page_number = int(request.GET.get('page'))

    # query_title_string = ""
    # if query_title is not None and len(query_title) > 0:
    #     query_title_string = "and ("
    #     for item in query_title.split(' '):
    #         query_title_string += f" title like '%{item}%' or"
    #
    #     query_title_string = query_title_string[:-3] + ")"
    #
    # query_desc_string = ""
    # if query_desc is not None and len(query_desc) > 0:
    #     query_desc_string = "and ("
    #     for item in query_desc.split(' '):
    #         query_desc_string += f" description like '%{item}%' or"
    #
    #     query_desc_string = query_desc_string[:-3] + ")"
    #
    # final_query = r"""SELECT * from search_api_youtube where 1=1 %s %s"""

    try:
        # search_results = Youtube.objects.raw(final_query, [query_title_string, query_desc_string])
        '''
        Search the stored videos using their title and description
        '''
        search_results = Youtube.objects.filter(title__icontains=query_title if query_title is not None else ''
                                                , description__contains=query_title if query_title is not None else '') \
            .order_by('-published_at')


        '''
        Pagination
        '''
        paginator = Paginator(search_results, 25)
        page_obj = paginator.get_page(page_number)


        '''
        Serializing results using Django Rest Framework
        '''
        serialized_results = YoutubeSerializer(page_obj.object_list, many=True)

        return JsonResponse({"result": serialized_results.data, "total_page": paginator.num_pages})
    except Exception as e:
        logging.error(e)
        return JsonResponse({"success": "failed", "result": e})
