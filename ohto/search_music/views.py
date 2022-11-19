from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from elasticsearch import Elasticsearch


class SearchView(APIView):

    def get(self, request):
        es = Elasticsearch(
            hosts=['localhost:9200'],
            http_auth=('elastic', 'changeme'),
        )

        # 검색어
        search_word = request.query_params.get('search')

        if not search_word:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'search word param is missing'})
        docs = es.search(index='music',
                         body={
                             "query": {
                                 "multi_match": {
                                     "query": search_word,
                                     "fields": [
                                         "title",
                                         "artist",
                                         "tag",
                                    ]
                                 }
                             }
                         })
        data_list = []
        for data in docs['hits']['hits']:
            data_list.append(data.get('_id'))
            data_list.append(data.get('_source'))

        return Response(data_list)