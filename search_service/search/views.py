from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps

from rest_framework import generics
from rest_framework.response import Response

from .models import Settings
from .serializers import ProfileSearchSerializer

from .profiles_rating import arrange_candidates
from .utilities import check_params
# Create your views here.


class Profile_Rate(generics.GenericAPIView):
    serializer_class = ProfileSearchSerializer

    def post(self, request, *args, **kwargs):
        settings = Settings.objects.first()
        if settings:
            if not settings.enabled:
                return Response({"Предупреждение": "Поиск запрещён администратором."})
        else:
            return Response({"Ошибка": "Параметры настройки сервиса не обнаружены."})

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"Ошибка": "Неверные параметры поискового запроса."})
        search_params = serializer.validated_data

        err = check_params(search_params)
        if err != '':
            return Response({"Ошибка в параметрах": err})

        return Response(arrange_candidates(search_params))
