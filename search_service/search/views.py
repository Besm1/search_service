from django.contrib.postgres.fields import ArrayField
from django.db.models import QuerySet, F, CharField
from django.db.models.functions import Cast
from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps

from rest_framework import generics
from rest_framework.response import Response
from .serializers import ProfileSearchSerializer
from search_service.utilities import clean_phone_number, NormalizePhoneNumbers

from .models import *
from prof.models import *
from .profiles_rating import arrange_candidates
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

def update_rates(rates, profiles) -> dict:
    curr_profiles = set(rates.keys())
    new_profiles = set(profiles)
    for p_ in curr_profiles - new_profiles: # удалим оценки лишних профилей
        del rates[p_]
    for p_ in curr_profiles & new_profiles: # увеличим оценки профилей, которые уже были и которые есть среди новых
        rates[p_] += 1
    for p_ in new_profiles - curr_profiles: # добавим оценки вновь появившихся профилей = 1
        rates[p_] = 1
    return rates


class ProfileSearchView(generics.GenericAPIView):
    serializer_class = ProfileSearchSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        profiles = ProfileProfile.objects.all()
            # .annotate(phone_for_search=NormalizePhoneNumbers(Cast(F('phone'), output_field=ArrayField(CharField())))))
        # Все профили. Их будем просеивать через фильтры поискового запроса
        rates = dict({})

        search_keys = list(data.keys()) # отсортируем параметры запроса по приоритету, как он задан в настройках
        search_keys.sort(key=lambda x: SearchParams.objects.get(name=x).priority)

        for param in search_keys:

            properties = SearchParams.objects.get(name=param) # свойства настройки параметра

            if param == 'profile_id' and data.get('profile_id', []):
                profiles = profiles.filter(user__in=data.get('profile_id', []))
                rates = update_rates(rates, profiles) # {profile.id: rates[profile.id]+1 if rates[profile.id] else 1 for profile in profiles}

            if param == 'username' and data.get('username', []):
                profiles = profiles.filter(username__in=data.get('username', []))
                rates = update_rates(rates, profiles)

            if param == 'tg_nick' and data.get('tg_nick', []):
                profiles = profiles.filter(tg_nick__in=data.get('tg_nick', []))
                rates = update_rates(rates, profiles)

            if param == 'email' and data.get('email', []):
                profiles = profiles.filter(email__in=data.get('email', []))
                rates = update_rates(rates, profiles)

            if param == 'last_name' and data.get('last_name', []):
                profiles = profiles.filter(email__in=data.get('last_name', []))
                rates = update_rates(rates, profiles)

            if param == 'first_name' and data.get('first_name', []):
                profiles = profiles.filter(email__in=data.get('first_name', []))
                rates = update_rates(rates, profiles)

            if param == 'phone':
                profiles = profiles.filter(phone__contains=clean_phone_number(data.get('phone', [])))
                rates = update_rates(rates, profiles)

            if param =='location':
                profiles = profiles.filter(location__in=data.get('location', []))
                rates = update_rates(rates, profiles)


            # Поиск кандидатов с необходимыми навыками
            candidate_ids = set()
            for profile in profiles:
                # user_skills = ProfileUserskill.objects.filter(user=profile, skill_name__in=skills).values_list('skill_name',
                user_skills = ProfileUserskill.objects.filter(user=profile).values_list('skill_name', flat=True)

                # Если все требуемые навыки найдены, добавляем кандидата в результат
                if set(data.get('skill', [])).issubset(set(user_skills)):
                    candidate_ids.add(profile.id)

            # Добавляем фильтрацию по образованию, если она указана
            if param == 'college':
                colleges = data.get('college', [])

                filtered_profiles = []
                for candidate_id in candidate_ids:
                    profile_education = ProfileEducationuser.objects.filter(
                        user=candidate_id,
                        college__in=colleges
                    )
                    if profile_education.exists():
                        filtered_profiles.append(candidate_id)

                candidate_ids = filtered_profiles

        # Возвращаем результат в виде списка user_id
        response_data = {"candidates": list(candidate_ids)}
        return Response(response_data)

class Profile_Rate(generics.GenericAPIView):
    serializer_class = ProfileSearchSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"error": "Invalid search parameters"})
        search_request = serializer.validated_data

        return Response(arrange_candidates(search_request))
