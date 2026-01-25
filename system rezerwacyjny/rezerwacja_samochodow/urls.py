from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register(r'cars', CarViewSet, basename='car')
router.register(r'reservations', ReservationViewSet, basename='reservations')
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home_a'),
    # Rejestracja i logowanie - to brakowało
    path('register/', RegisterViewSet.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # Moje dodatkowe endpointy
    path('report/monthly/<int:month>/', MonthlyReport.as_view()),
    path('cars/starts-with/<str:letter>/', CarsStartingWith.as_view()),
    path('my-reservations/', UserReservationsList.as_view()),
    path('api/', include(router.urls)),
    #path('/reservation/create/', views.Reservation_create, name='home_a'),
]