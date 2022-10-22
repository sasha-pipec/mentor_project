from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from photobatle import serializers
from photobatle.service import *


class PaginationAjax(APIView):
    swagger_schema = None

    def get(self, request, *args, **kwargs):
        try:
            if 'user_id' in request.GET:
                posts = PersonalPaginationService.execute(request.GET)
            else:
                posts = PaginationService.execute(request.GET)
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data,
                             'active_page': self.request.GET['page']}, status=200)


class SortingFormAjax(APIView):
    """Class for AJAX request sorting"""
    swagger_schema = None

    def post(self, request, *args, **kwargs):
        # We get the value of the form by which we will sort
        try:
            posts = SortingFormService.execute(request.POST)
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data,
                             'active_page': self.request.POST['page']}, status=200)


class SearchFormAjax(APIView):
    """Class for AJAX query"""
    swagger_schema = None

    def post(self, request, *args, **kwargs):
        try:
            data = SearchFormService.execute(request.POST)
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'posts': serializers.PhotoSerializer(data['photos'], many=True).data,
                             'active_page': self.request.POST['page'],
                             'max_page': data['max_page']}, status=200)


class PersonalSortingFormAjax(APIView):
    """Class for AJAX request sorting personal list posts"""
    swagger_schema = None

    def post(self, request, *args, **kwargs):
        try:
            data = PersonalSortingFormService.execute(request.POST)
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'posts': serializers.PhotoSerializer(data['photos'], many=True).data,
                             'active_page': self.request.POST['page'],
                             'max_page': data['max_page']}, status=200)
