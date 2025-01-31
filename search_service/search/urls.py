from django.urls import path
from .views import * #show_models_n_fields

urlpatterns = [
    path('search/', dummy_page),
    path('search/models/', show_models_n_fields),
    path('api/search/', ProfileSearchView.as_view())
]
