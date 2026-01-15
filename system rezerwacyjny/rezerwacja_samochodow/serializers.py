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
class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = '__all__'

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
#sprawdzam i nie tykam