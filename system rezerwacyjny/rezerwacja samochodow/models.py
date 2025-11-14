from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationsError
from datetime import date

#Wybór typu auta (hybrydowe,elektryczne,spalinowe)
class Car(models.Model)
car_types = (
    ('H', 'Hybrydowe'),
    ('E', 'Elektryczne'),
    ('S', 'Spalinowe'),
)

car_name = models.CharField(max_length=50)
car_types = models.CharField(max_length=1, choices=car_types)
car_registration = models.CharField(max_length=7)