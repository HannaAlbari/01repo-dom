from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
#Mój widok
from rest_framework.views import APIView
#szybkie tworzenie kompletnych CRUD
from rest_framework import viewsets, generics
#zwracanie danych JSON
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from .serializers import *
from .forms import *
#from .permissions import IsAdminOrReadOnly

# lecimy z rezerwacjami - rejestracja osoby do api z ograniczeniem (he he umysłowym)
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
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]  # Tylko admin
        return [IsAuthenticated()]  # Wszyscy zalogowani
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
    permission_classes = [IsAdminUser]
    def get(self, request, month):
        count = Reservation.objects.filter(date_from__month=month).count()
        return Response({"month": month, "reservations": count})

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
#przerobić na class!!!! <-Jednak zostawiam Ufff 
def home_view(request):
    return render(request, 'rezerwacja_samochodow/home.html')


def register_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'rezerwacja_samochodow/auth/register.html',
    {'form': form}
    )


@staff_member_required
def create_car_view(request):
    return render(request, 'rezerwacja_samochodow/cars/create.html')

def detail_view(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'rezerwacja_samochodow/cars/detail.html', {'car': car})

def list_view(request):
    cars = Car.objects.all()
    return render(request, 'rezerwacja_samochodow/cars/list.html', {'cars': cars})

@login_required(login_url='login')
def create_reservations_view(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        
        try:
            car = Car.objects.get(pk=car_id)
            
            reservation = Reservation.objects.create(
                user=request.user,
                car=car,
                date_from=date_from,
                date_to=date_to
            )
            
            messages.success(request, 'Rezerwacja została pomyślnie utworzona!')
            return redirect('user_list_view')  # przekierowanie do listy rezerwacji użytkownika
            
        except Car.DoesNotExist:
            return render(request, 'rezerwacja_samochodow/reservations/create.html', {
                'cars': Car.objects.all(),
                'error': 'Wybrany samochód nie istnieje'
            })
        except ValidationError as e:
            return render(request, 'rezerwacja_samochodow/reservations/create.html', {
                'cars': Car.objects.all(),
                'error': str(e)
            })
    
    cars = Car.objects.all()
    return render(request, 'rezerwacja_samochodow/reservations/create.html', {'cars': cars})

def user_list_view(request):
    reservations = Reservation.objects.filter(user=request.user) 
    return render(request, 'rezerwacja_samochodow/reservations/user_list.html',
                  {'reservation': reservations})  

def logout_view(request):
    logout(request)
    return redirect('home')


#zobaczymy czy zadziała
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    # Jeśli użytkownik już zalogowany, przekieruj
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Debug - usuń po sprawdzeniu
        print(f"Próba logowania: {username}")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Zalogowano pomyślnie!')
            return redirect('home')
        else:
            return render(request, 'rezerwacja_samochodow/auth/login.html', {
                'error': 'Nieprawidłowa nazwa użytkownika lub hasło'
            })
    
    return render(request, 'rezerwacja_samochodow/auth/login.html')
