"""
URL configuration for projekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'brands', CarBrandViewSet)
router.register(r'cars', CarViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Rejestracja i logowanie - to brakowało
    path('register/', RegisterSerializer.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # Moje dodatkowe endpointy
    path('report/monthly/<int:month>/', MonthlyReport.as_view()),
    path('cars/starts-with/<str:letter>/', CarsStartingWith.as_view()),
    path('my-reservations/', UserReservationsList.as_view()), # Lista rezerwacji usera
]