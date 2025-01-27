from django.contrib import admin

# Register your models here.
from .models import *
from .views import Profile_Model, Profile_Field, get_models_list


def import_profile_fields(modeladmin, request, queryset):
    Fields.objects.all().delete()
    models = get_models_list('prof')
    for model in models:
        for field in model.fields:
            Fields.objects.create(model_name=model.name, field_name=field.name, field_type=field.type)


admin.site.register(Settings)


@admin.register(Fields)
class FieldsAdmin(admin.ModelAdmin):
    actions = [import_profile_fields]


