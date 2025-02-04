from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps

from rest_framework import generics
from rest_framework.response import Response
from .serializers import ProfileSearchSerializer

from .profiles_rating import arrange_candidates
# Create your views here.

class Profile_Rate(generics.GenericAPIView):
    serializer_class = ProfileSearchSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"error": "Invalid search parameters"})
        search_request = serializer.validated_data

        return Response(arrange_candidates(search_request))
