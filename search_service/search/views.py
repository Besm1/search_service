from pprint import pprint

from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps
from django.db import models

from rest_framework import generics
from rest_framework.response import Response
from .serializers import ProfileSearchSerializer
import json


from .models import *
from prof.models import *

# Create your views here.

class Profile_Field:
    def __init__(self, name:str, type_descr:str):
        self.name = name
        self.type = type_descr

class Profile_Model:
    def __init__(self, name:str, fields:list):
        self.name = name
        self.fields = fields

    def __str__(self):
        return f'{self.name}: {self.fields}'

def get_models_list(app:str) -> list:
    models = apps.get_app_config(app).get_models()

    # Создаем словарь, где ключами будут имена моделей,
    # а значениями - списки имен полей этих моделей
    model_fields_list = []
    for model in [m_ for m_ in models if not (m_.__name__.startswith('Auth') or m_.__name__.startswith('Django'))]:
        # Имя модели
        model_name = model.__name__

        # Список имен полей модели
        field_names = [Profile_Field(field.name, str(type(field).description)[:50])
                       for field in model._meta.fields]
        # print([f'{field.name}: {type(field).description}\n' for field in model._meta.fields])

        # Добавляем модель и её поля в словарь
        model_fields_list.append(Profile_Model(model_name, field_names))
    return model_fields_list

def show_models_n_fields(request):
    models = get_models_list('prof')
    # pprint(models)
    return render(request, 'search/models_n_fields.html', context = {'models': models})

def dummy_page(request):
    # Получаем все модели из приложения 'search'
    # models = get_models_list('prof')
    # print(models)
    # pprint(ProfileUser.objects.all())
    # pprint(Fields.objects.all())
    return HttpResponse('Welcome to search service!')


class ProfileSearchView(generics.GenericAPIView):
    serializer_class = ProfileSearchSerializer

    # def post(self, request, *args, **kwargs):
        # # Получаем данные из тела запроса
        # data = json.loads(request.body.decode("utf-8"))
        #
        # # Проверяем наличие необходимых полей
        # required_fields = ["location", "skills"]
        # for field in required_fields:
        #     if field not in data:
        #         return Response({"error": f"{field} is a required field."}, status=400)
        #
        # # Извлекаем значения полей
        # locations = data.get("location")
        # skills = data.get("skills")
        #
        # # Логика поиска кандидатов
        # candidates = self.search_candidates(locations, skills)
        #
        # # Возвращаем результат в виде списка user_id
        # response_data = {"candidates": candidates}
        # return Response(response_data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Логика поиска кандидатов
        # Фильтрация по местоположению
        locations = data.get('location', [])
        skills = data.get('skills', [])

        candidates = self.search_candidates(locations, skills)

        # Возвращаем результат в виде списка user_id
        response_data = {"candidates": candidates}
        return Response(response_data)



    def search_candidates(self, locations, skills, education=None):
        """
        Метод для поиска кандидатов по заданным параметрам
        :param locations: Список городов, где должны находиться кандидаты
        :param skills: Список требуемых навыков
        :param education: Словарь с требованиями к образованию
        :return: Список user_id подходящих кандидатов
        """
        # Поиск кандидатов по местоположению
        profiles = ProfileProfile.objects.all()
        if locations:
            profiles = profiles.filter(location__in=locations)

        # Поиск кандидатов с необходимыми навыками
        candidate_ids = set()
        for profile in profiles:
            user_skills = ProfileUserskill.objects.filter(user=profile, skill_name__in=skills).values_list('skill_name',
                                                                                                           flat=True)

            # Если все требуемые навыки найдены, добавляем кандидата в результат
            if set(skills).issubset(set(user_skills)):
                candidate_ids.add(profile.id)

        # Добавляем фильтрацию по образованию, если она указана
        if education:
            specialities = education.get('specialities')
            colleges = education.get('colleges')

            filtered_profiles = []
            for candidate_id in candidate_ids:
                profile_education = ProfileEducationuser.objects.filter(
                    user=candidate_id,
                    speciality__in=specialities,
                    college__in=colleges
                )
                if profile_education.exists():
                    filtered_profiles.append(candidate_id)

            candidate_ids = filtered_profiles

        return list(candidate_ids)
