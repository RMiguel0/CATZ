from django.db import models
import requests

mapbox_access_token = 'pk.eyJ1IjoibXJpdmVybzAwIiwiYSI6ImNsbG11NWptbjF0ZmIzcXI2dDdybThnMmkifQ.uhdlXK3odioAdWo0OOogwA'


# Create your models here.
class Direcciones(models.Model):
    Direccion = models.TextField()
    Lat = models.FloatField()
    Long = models.FloatField()

    def procesar_direccion(request):
        self.Direccion = direccion

    def obtener_coordenadas(self):
        url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{self.Direccion}.json?'
        param = {
            'access_token': mapbox_access_token,
            'country': 'CL',
            'limit': 1
        }
        respuesta = requests.get(url, params=param)
        data = respuesta.json()
        coords = data['features'][0]['geometry']['coordinates']
        coords.reverse()
        return coords
    
    def __str__(self):
        return str(self.obtener_coordenadas())