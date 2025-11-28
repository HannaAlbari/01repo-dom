from django.shortcuts import render

#Mój widok
from rest_framework.views import APIView
#szybkie tworzenie kompletnych CRUD
from rest_framework import viewsets, generics
#zwracanie danych JSON
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import *
from .serializers import *
from .permissions import IsAdminOrReadOnly