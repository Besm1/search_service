from django.db import models

# Create your models here.

class Settings(models.Model):
    enabled = models.BooleanField(default=True)


class Fields(models.Model):
    SEARCH_TYPES = (('EQUAL', 'Совпадение'), ('SUBSTR', 'Поиск подстроки')
                    , ('AGE', 'Попадание д.р. в нужный диапазон возрастов'))
    MSEARCH_TYPES = (('ANY', 'Хотя бы одно качество входит в поисковый запрос')
                    , ('ALL', 'Есть все качества из поискового запроса'))

    model_name = models.CharField(max_length=32, blank=True)
    field_name = models.CharField(max_length=32, blank=True)
    field_type = models.CharField(max_length=50, blank=True)
    search_enabled = models.BooleanField(default=True)
    search_weight = models.FloatField(default=1, blank=True)
    search_type = models.CharField(max_length=10, choices=SEARCH_TYPES,default='EQUAL')
    mult_search_type = models.CharField(max_length=3, choices=MSEARCH_TYPES, default='ANY')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['model_name', 'field_name'], name='unique_model_and_field_name')]

class SearchParams(models.Model):
    SEARCH_TYPES = (('EQUAL', 'Совпадение'), ('SUBSTR', 'Поиск подстроки')
                    , ('AGE', 'Попадание д.р. в нужный диапазон возрастов'))
    MSEARCH_TYPES = (('ANY', 'Хотя бы одно качество входит в поисковый запрос')
                    , ('ALL', 'Есть все качества из поискового запроса'))

    priority = models.IntegerField(default=0)
    name = models.CharField(max_length=32, blank=True, unique=True)
    enabled = models.BooleanField(default=True)
    weight = models.FloatField(default=1, blank=True)
    search_type = models.CharField(max_length=10, choices=SEARCH_TYPES,default='EQUAL')
    mult_search_type = models.CharField(max_length=3, choices=MSEARCH_TYPES, default='ANY')
