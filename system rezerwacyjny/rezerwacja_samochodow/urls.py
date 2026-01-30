from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register(r'cars', CarViewSet, basename='car')
router.register(r'reservations', ReservationViewSet, basename='reservations')
router.register(r'reviews', ReviewViewSet, basename='reviews')


urlpatterns = [
    path('', views.home_view, name='home'),  # zostaw tylko jeden
    # path('home/', views.home_view, name='home_view'),  # usuń lub zostaw ten
    
    path('cars/', views.list_view, name='car_list_html'),
    path('cars/<int:pk>/', views.detail_view, name='car_detail_html'),  # dodaj "/" na końcu
    path('cars/create/', views.create_car_view, name='create_car_html'),  # zmieniona ścieżka
    path('register-page/', views.register_view, name='register_html'),
    path('logout/', views.logout_view, name='logout'),
    path('login-page/', views.login_view, name='login_html'),
    path('reservations/create', views.create_reservations_view, name='create_reservations_html'),  # zmieniona
    path('my-reservations/', views.user_list_view, name='user_list_view'),

    # API URLs
    path('api/register/', RegisterViewSet.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/report/monthly/<int:month>/', MonthlyReport.as_view()),
    path('api/my-reservations/', UserReservationsList.as_view()),
    ]
