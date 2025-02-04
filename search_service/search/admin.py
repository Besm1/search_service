from django.contrib import admin

# Register your models here.
from .models import *
from .generate_fakedata import generate_fake_data

admin.site.register(Settings)

@admin.register(SearchParams)
class SearchParamsAdmin(admin.ModelAdmin):
    actions = [                 # import_profile_fields ,
               generate_fake_data
              ]


