#utworzone po to żeby było czytelen model.. to moja baza danych views to część chyba logiczna... 
#ma odpowiadać za walidacje i tłyumaczenie klas na to coś JSON i odwrotnie
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

# Do rejestracji - tworzenie konta,
# hasła pa pa i do serwera (i do pieca xd)
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
# po prostu zapisuje dane bo musi zahashować hasło i zamienić je na coś innego
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

# Podstawowe serializatory dla modeli
# Niemiecki Bauer mówi to coś jest do tego czegoś
#Dane zamieni na tego JSON

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

from rest_framework import serializers
from datetime import date

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
    
    def validate_start_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Data nie może być z przeszłości")
        return value
    
    def validate(self, data):
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("Data końcowa musi być po dacie początkowej")
        return data

def validate(self, data):
    # Sprawdź czy auto jest dostępne w tym terminie
    overlapping = Reservation.objects.filter(
        car=data['car'],
        start_date__lt=data['end_date'],
        end_date__gt=data['start_date']
    )
    if overlapping.exists():
        raise serializers.ValidationError("Auto zajęte w tym terminie")
    return data
#sprawdzam i nie tykam