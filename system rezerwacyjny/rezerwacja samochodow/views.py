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

# lecimy z rezerwacjami
class RegisterSerializer(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=request.data["username"])
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

# crud _ dalej trzeba zobacztć co to?!!@!\
#Określa wszystkie obiekty modelu CarBrand, będą dostępne poprzez ten ViewSet.
#Określa serializator używany do obiektów CarBrand (walidacja danych wejsciowych chyba)
#Definiuje uprawnienia dostępu: (administratorzy mogą tworzyć, aktualizować lub usuwać (POST, PUT, PATCH, DELETE).) inni tylko GET
class CarBrandViewSet(viewsets.ModelViewSet):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer
    permission_classes = [IsAdminOrReadOnly]
#Dotyczy modelu Reservation 
#Tylko zalogowani (uwierzytelnieni) użytkownicy mogą wykonywać odczyt, tworzenie, aktualizacja, usuwanie na !rezerwacjach!
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminOrReadOnly]
#Dotyczy modelu Reservation
#Tylko zalogowani (uwierzytelnieni) użytkownicy mogą odczyt, tworzenie, aktualizacja, usuwanie na rezerwacjach
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
#Dotyczy modelu Review
#tylko zalogowani użytkownicy mogą dodawać lub przeglądać recenzje.
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

#Endpointy te dodatkowe nie wiem jak je nazwać 
#Ta klasa do pobierania liczby rezerwacji w danym miesiącu.
class MonthlyReport(APIView):
    def get(self, request, month):
        count = Reservation.objects.filter(date_from__month=month).count
        return Response({"month": month, "reservations": count})
#klasa do pobierania listy samochodów, których model zaczyna się na określoną literę.
class CarsStartingWith(APIView):
   def get(self, request, letter):
        cars = Car.objects.filter(model__istartswith=letter)
        return Response(CarSerializer(cars, many=True).data)

 




    
