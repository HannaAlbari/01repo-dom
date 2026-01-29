#klasy prezentujace tabele w bazie danych
from django.db import models
#model uzytkownika django
from django.contrib.auth.models import User
#kiedy walidacja danych nie przejdzie 
from django.core.exceptions import ValidationError
#obsługa czasu i dat
from django.utils import timezone
#działanie z datammi
from datetime import date

#model1.user profile/profil użytkownika
 
class Profile(models.Model):
    ROLE_CHOICES = (('admin', 'administrator'), ('user', 'użytkownik'),)
#każdy profil nalezy do jednego uzytkownika troche profil uzytkownika to rozszerzenie, usunięcie uzytkownika = usuniecie konta, jesli nie podasz roli to automatycznie przypisany jest user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
#dodaj nazwisko bla bla bla  
    def __str__(self):
        return f"{self.user.username} ({self.role})"

#model3.wybor modeli samochodu
#marka samochodu wyświetlanie obiektu jako tekst - marki(......?) 

class Car(models.Model):
    DRIVE_TYPES = (('E', 'Elektryczny'),('H', 'Hybrydowy'),('S', 'Spalinowy'),)
#wiele aut do jednej marki to to co było wielw do jednego
    brand = models.CharField(max_length=50, unique=True)
    model = models.CharField(max_length=20)
    year = models.PositiveIntegerField()

#automatycznie przypisany samochod spalinowy jesli uzytkownik nie wybierze nic
    Car_TYPES = models.CharField(max_length=20, choices=DRIVE_TYPES, default='Spalinowy')
    
    def __str__(self):
        return f"{self.brand.name} {self.model} ({self.year})- {self.get_drive_type_display()}"

#model4.  model rezerwacji
def validate_future(value):
    if value < date.today():
        raise ValidationError("Data zakończenia nie może być przeszła")

class Reservation(models.Model):
#Rezerwacja należy do konkretnego użytkownika systemu.ForeignKey oznacza relację wiele do jednego.Każdy użytkownik może mieć wiele rezerwacji.
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    car = models.ForeignKey(Car, on_delete = models.CASCADE) 
    date_from = models.DateField(validators = [validate_future])
    date_to = models.DateField(validators = [validate_future])
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user.username} -> {self.car}"

def clean(self):
    if self.date_to < self.date_from:
        raise ValidationError("Data zakończeni musi być później niż rozpoczęcia.")


#model5. model recenzji auta

class Review(models.Model):
#kto pisze recenzje/ relacja wiele do jednego/ gdy użytkownik zostanie usunięty jego recenzje też pa pa.
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    car = models.ForeignKey(Car, on_delete = models.CASCADE) 
#przechowanie ocen samochodów 
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f" ocena{self.rating}/5 dla {self.car}"


