from pprint import pprint

from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps
from django.db import models

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
    pprint(ProfileUser.objects.all())
    pprint(Fields.objects.all())
    return HttpResponse('Welcome to search service!')