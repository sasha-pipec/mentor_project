from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from photobatle.serializers import *
from photobatle.services import *


class PaginationAjax(APIView):
    swagger_schema = None

    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                PaginationService, request.GET
            )
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse(
            {
                'posts': PhotoSerializer(outcome.result, many=True).data,
                'active_page': self.request.GET['page']
            }, status=200
        )


class SortingFormAjax(APIView):
    """Class for AJAX request sorting"""
    swagger_schema = None

    def get(self, request, *args, **kwargs):
        # We get the value of the form by which we will sort
        try:
            outcome = ServiceOutcome(
                PaginationService, request.GET
            )
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse(
            {
                'posts': PhotoSerializer(outcome.result, many=True).data,
                'active_page': self.request.GET['page']
            }, status=200
        )


class SearchFormAjax(APIView):
    """Class for AJAX query"""
    swagger_schema = None

    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                PaginationService, request.GET
            )
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse(
            {
                'posts': PhotoSerializer(outcome.result, many=True).data,
                'active_page': self.request.GET['page'],
                'max_page': outcome.result.paginator.page_range.stop - 1
            }, status=status.HTTP_200_OK
        )


class PersonalSortingFormAjax(APIView):
    """Class for AJAX request sorting personal list posts"""
    swagger_schema = None

    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                PaginationService, request.GET
            )
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse(
            {
                'posts': PhotoSerializer(outcome.result.object_list, many=True).data,
                'active_page': self.request.GET['page'],
                'max_page': outcome.result.paginator.page_range.stop - 1
            }, status=status.HTTP_200_OK
        )
