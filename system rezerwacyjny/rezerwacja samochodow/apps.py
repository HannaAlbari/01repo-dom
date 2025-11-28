#importuje sobie klase AppConfig do konfigurowania aplikacji
from django.apps import AppConfig

#Rejestruje aplikację, Nadaje jej nazwę, Ustawia typ domyślnego ID
class BibliotekaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservations'