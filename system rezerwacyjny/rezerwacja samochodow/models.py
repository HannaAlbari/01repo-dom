#klasy prezentujace tabele w bazie danych
from django.db import models
#model uzytkownika django
from django.contrib.auth.models import User
#kiedy walidacja danych nie przejdzie 
from django.core.exceptions import ValidationsError
#obsługa czasu i dat
from django.utils import timezone
#model1.

#user profile/profil użytkownika 
class Profile(models.Model):
    ROLE_CHOICES = (('admin', 'administrator'), ('user', 'użytkownik'),)
#każdy profil nalezy do jednego uzytkownika troche profil uzytkownika to rozszerzenie, usunięcie uzytkownika = usuniecie konta, jesli nie podasz roli to automatycznie przypisany jest user
user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    def __str__(self):
        return f"{self.user.username} ({self.role})"
#model2.

# marka samochodu wyświetlanie obiektu jako tekst - marki(......?)
class CarBrand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
#model3.

#wybor modeli samochodu
class Car(models.Model):
    Car_TYPES = (('E', 'Elektryczny'),('H', 'Hybrydowy'),('S', 'Spalinowy'),)
#wiele aut do jednej marki to to co było wielw do jednego
brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    model = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
#automatycznie przypisany samochod spalinowy jesli uzytkownik nie wybierze nic
    Car_TYPES = models.CharField(max_length=20, choices=DRIVE_TYPES, default='Spalinowy')
    def __str__(self):
        return f"{self.brand.name} {self.model} ({self.year})- {self.get_drive_type_display()}""