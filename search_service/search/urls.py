from django.urls import path
from .views import * #show_models_n_fields

urlpatterns = [
    path('api/search/', Profile_Rate.as_view())
]
