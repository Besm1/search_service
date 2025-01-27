from django.urls import path
from .views import * #show_models_n_fields

urlpatterns = [
    path('', dummy_page),
    path('show_models/', show_models_n_fields),
]
