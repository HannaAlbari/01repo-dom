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
#from .permissions import IsAdminOrReadOnly

# lecimy z rezerwacjami
class RegisterViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=request.data["username"])
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

# crud _ dalej trzeba zobacztć co to?!!@!\ <--- już wiem
#Określa wszystkie obiekty modelu CarBrand, będą dostępne poprzez ten ViewSet.
#Określa serializator używany do obiektów CarBrand (walidacja danych wejsciowych chyba)
#Definiuje uprawnienia dostępu: (administratorzy mogą tworzyć, aktualizować lub usuwać (POST, PUT, PATCH, DELETE).) inni tylko GET
#class CarBrandViewSet(viewsets.ModelViewSet):
    #queryset = CarBrand.objects.all()
    #serializer_class = CarBrandSerializer
    #permission_classes = [IsAdminOrReadOnly]
#Dotyczy modelu Reservation 
#Tylko zalogowani (uwierzytelnieni) użytkownicy mogą wykonywać odczyt, tworzenie, aktualizacja, usuwanie na !rezerwacjach!
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    #permission_classes = [IsAdminOrReadOnly]
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
        count = Reservation.objects.filter(date_from__month=month).count()
        return Response({"month": month, "reservations": count})
#klasa do pobierania listy samochodów, których model zaczyna się na określoną literę.
class CarsStartingWith(APIView):
   def get(self, request, letter):
        cars = Car.objects.filter(model__istartswith=letter)
        return Response(CarSerializer(cars, many=True).data)

from django.contrib.auth import authenticate
#ochrona sprawdzanie czu ten któś istnieje i czy hasło jest ok
from rest_framework import status
#nr błędów (jak moja obecność na informatyce) zamienia na czytelne nazwy

# Logowanie (to chyba zwraca token?!) oby tak to działało
# zwraca token
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Błędne dane logowania"}, status=status.HTTP_400_BAD_REQUEST)

# Drugi endpoint poza CRUD - Lista rezerwacji aktualnego użytkownika
# Endpoint "Tylko dla mnie" jakiś kowalski nie zobaczy rezerwacji Nowaka 
class UserReservationsList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        reservations = Reservation.objects.filter(user=request.user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)
 
# views.py

def home_view(request):
    return render(request, 'rezerwacja_samochodow/home.html')



    
