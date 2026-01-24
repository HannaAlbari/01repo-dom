#To włącza funkcje odpowiedzialne za panel admina 
from django.contrib import admin
#modele z pliku models.py pobiera sobie
from .models import Profile, Car, Reservation, Review

admin.site.register(Profile)
admin.site.register(Car)
admin.site.register(Reservation)
admin.site.register(Review)

##GOTOWE TEGO NIE TYKAM 