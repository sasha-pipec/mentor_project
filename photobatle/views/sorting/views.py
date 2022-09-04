from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from photobatle import serializers
from photobatle.service import *


class SortingFormAjax(APIView):
    """Class for AJAX request sorting"""
    swagger_schema = None

    def post(self, request, *args, **kwargs):
        # We get the value of the form by which we will sort
        try:
            posts = SortingFormService.execute(request.POST)
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)


class SearchFormAjax(APIView):
    """Class for AJAX query"""
    swagger_schema = None

    def post(self, request, *args, **kwargs):
        try:
            posts = SearchFormService.execute(request.POST)
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)


class PersonalSortingFormAjax(APIView):
    """Class for AJAX request sorting personal list posts"""
    swagger_schema = None

    def post(self, request, *args, **kwargs):
        try:
            posts = PersonalSortingFormService.execute(request.POST)
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)
