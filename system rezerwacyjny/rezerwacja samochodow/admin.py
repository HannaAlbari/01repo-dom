#To włącza funkcje odpowiedzialne za panel admina 
from django.contrib import admin
#modele z pliku models.py pobiera sobie
from .models import Profile, CarBrand, Car, Reservation, Review

admin.site.register(Profile)
admin.site.register(CarBrand)
admin.site.register(Car)
admin.site.register(Reservation)
admin.site.register(Review)
