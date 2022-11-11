from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from photobatle.serializers import *
from photobatle.service import *


class PaginationAjax(APIView):
    swagger_schema = None

    def get(self, request, *args, **kwargs):
        try:
            if 'user_id' in request.GET:
                outcome = ServiceOutcome(
                    PersonalPaginationService, request.GET
                )
            else:
                outcome = ServiceOutcome(
                    PaginationService, request.GET
                )
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'posts': PhotoSerializer(outcome.result, many=True).data,
                             'active_page': self.request.GET['page']}, status=200)


class SortingFormAjax(APIView):
    """Class for AJAX request sorting"""
    swagger_schema = None

    def post(self, request, *args, **kwargs):
        # We get the value of the form by which we will sort
        try:
            outcome = ServiceOutcome(
                SortingFormService, request.POST
            )
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'posts': PhotoSerializer(outcome.result, many=True).data,
                             'active_page': self.request.POST['page']}, status=200)


class SearchFormAjax(APIView):
    """Class for AJAX query"""
    swagger_schema = None

    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                SearchFormService, request.POST
            )
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'posts': PhotoSerializer(outcome.result['photos'], many=True).data,
                             'active_page': self.request.POST['page'],
                             'max_page': outcome.result['max_page']}, status=status.HTTP_200_OK)


class PersonalSortingFormAjax(APIView):
    """Class for AJAX request sorting personal list posts"""
    swagger_schema = None

    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                PersonalSortingFormService, request.POST
            )
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'posts': PhotoSerializer(outcome.result['photos'], many=True).data,
                             'active_page': self.request.POST['page'],
                             'max_page': outcome.result['max_page']}, status=status.HTTP_200_OK)
