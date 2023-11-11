from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
import requests, os
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ubicaciones


# Create your views here.


def home(request):
    ubicacion = request.POST.get('city')
    print(ubicacion)
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'singup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('profile')
            except IntegrityError:
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya existe.'
                })
        return render(request, 'singup.html', {
            'form': UserCreationForm,
            'error': 'Contraseñas no coinciden.'
        })


@csrf_exempt
@login_required
def profile(request):
    user = request.user
    if request.method =='POST':
        ubicacion = request.POST.get('city')
        coordenadas = obtener_coordenadas(ubicacion)
        lat = coordenadas[0]
        longi = coordenadas[1]
        nuevo_usuario = ubicaciones(Direccion= ubicacion, Lat= lat, Long= longi, user=user)
        nuevo_usuario.save()
        #return JsonResponse({'success': True})
    try:
        direcciones = ubicaciones.objects.filter(user=user)
        atributos_ubicaciones = []

        # Itera sobre las direcciones y almacena sus atributos en la lista
        for ubicaciones in direcciones:
            atributos_direccion = {
                'direccion': ubicaciones.Direccion,
                #'latitud': direccion.Lat,
                #'longitud': direccion.Long,
                # Agrega más atributos según sea necesario
            }
            atributos_ubicaciones.append(atributos_direccion)
    except ubicaciones.DoesNotExist:
        # Manejar el caso en el que no se encuentra ninguna dirección
        atributos_direcciones = None
    return render(request, 'profile.html',{
        'direcciones': atributos_direcciones,
    })


def singout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'singin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'singin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta.'
            })
        else:
            login(request, user)
            return redirect('home')
        

def clima(request):
    return render(request, "clima.html")


mapbox_access_token = 'pk.eyJ1IjoibXJpdmVybzAwIiwiYSI6ImNsbG11NWptbjF0ZmIzcXI2dDdybThnMmkifQ.uhdlXK3odioAdWo0OOogwA'
def obtener_coordenadas(dirección):
    url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{dirección}.json?'

    param = {
    'access_token': mapbox_access_token,
    'limit': 1,
    'country': 'cl'
    }

    respuesta = requests.get(url, params=param)

    data = respuesta.json()

    if 'features' in data and len(data['features']) > 0:
        coordinates = data['features'][0]['geometry']['coordinates']
        coordinates.reverse()
        return coordinates
    else:
        return None


token_aqi = "a9fa736d75e0f33dc4a9ba18292eab99fa46eb4d"
def calidad_coor(coords):
    url = f'https://api.waqi.info/feed/geo:{coords[0]};{coords[1]}/?token=a9fa736d75e0f33dc4a9ba18292eab99fa46eb4d'
    res = requests.get(url)
    data = res.json()
    return data


def obtener_calidad_aire(ciudad, token_aqi):
    direccion = ciudad
    base_url = "https://api.waqi.info/feed/"
    url = f"{base_url}{direccion}/?token={token_aqi}"
    dic = {}

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get("status") == "ok":
            calidad_aire = data["data"]["aqi"]
            code = data['data']['idx']
            if 'pm10' not in data['data']['iaqi']:
                    pm10 = 'No se encontro registro'
            else:
                pm10 = data['data']['iaqi']['pm10']['v']
            if 'pm25' not in data['data']['iaqi']:
                pm25 = 'No se encontro registro'
            else:
                pm25 = data['data']['iaqi']['pm25']['v']
            print(f"La calidad aire del aire en {direccion} es: {calidad_aire}, codigo{code}")

            # Ahora, enviamos la calidad_aire del aire a OpenAI para obtener una respuesta_ai
            respuesta_ai = enviarCalidadAirea(calidad_aire)
            dic['aqi'] = calidad_aire
            dic['res'] = respuesta_ai['res']
            dic['description'] = respuesta_ai['calidad']
            dic['pm10'] = pm10
            dic['pm25'] = pm25
            return dic
        
        elif data.get('status') == 'error' and data['data'] == 'Unknown station':
            coords = obtener_coordenadas(direccion)
            if coords != None:
                data = calidad_coor(coords)
                calidad_aire = data["data"]["aqi"]
                code = data['data']['idx']
                if 'pm10' not in data['data']['iaqi']:
                    pm10 = 'No se encontro registro'
                else:
                    pm10 = data['data']['iaqi']['pm10']['v']
                if 'pm25' not in data['data']['iaqi']:
                    pm25 = 'No se encontro registro'
                else:
                    pm25 = data['data']['iaqi']['pm25']['v']
                print(f"La calidad aire del aire en {direccion} es: {calidad_aire}, codigo{code}")
                respuesta_ai = enviarCalidadAirea(calidad_aire)
                dic['aqi'] = calidad_aire
                dic['res'] = respuesta_ai['res']
                dic['description'] = respuesta_ai['calidad']
                dic['pm10'] = pm10
                dic['pm25'] = pm25
                return dic
            else:
                return JsonResponse({'error': 'No se pudo obtener la información de calidad aire del aire. Por favor probar con una ubicación mayor (Vecindario --> Comuna)'})

        else:
            print("No se pudo obtener la información de calidad aire del aire.")
            return JsonResponse({'error': 'No se pudo obtener la información de calidad aire del aire.'})

    except Exception as e:
        print(f"Hubo un error al obtener la información: {e}")
        return JsonResponse({'error': f'Hubo un error al obtener la información: {e}'})


def enviarCalidadAirea(calidad_aire):
    if 0 <= calidad_aire <= 50:
        res = {'res':'La calidad aire del Aire es Buena, no se anticipan impactos a la salud cuando la calidad aire del aire se encuentra en este intervalo.','calidad': 'Excelente'}
        return res
    elif 51 <= calidad_aire <= 100:
        res = {'res':'La calidad aire del Aire es Moderada, La calidad aire del aire es aceptable; sin embargo, para algunos contaminantes puede haber un problema de salud moderado para un número muy pequeño de personas que son inusualmente sensibles a la contaminación del aire. Los niños y adultos activos y las personas con enfermedades respiratorias, como asma, deben limitar el esfuerzo prolongado al aire libre.', 'calidad': 'Moderada'}
        return res
    elif 101 <= calidad_aire <= 150:
        res = {'res':'La calidad aire del Aire No es saludable para grupos sensibles. Los miembros de grupos sensibles pueden experimentar efectos sobre la salud. No es probable que el público en general se vea afectado. Los niños y adultos activos y las personas con enfermedades respiratorias, como asma, deben limitar el esfuerzo prolongado al aire libre.', 'calidad': 'No saludables para grupos sensibles'}
        return res
    elif 151 <= calidad_aire <= 200:
        res = {'res': 'La calidad aire del Aire es insalubre.Todo el mundo puede empezar a experimentar efectos sobre la salud; Los miembros de grupos sensibles pueden experimentar efectos más graves para la salud. Los niños y adultos activos y las personas con enfermedades respiratorias, como asma, deben evitar el esfuerzo prolongado al aire libre; todos los demás, especialmente los niños, deben limitar el esfuerzo prolongado al aire libre.','calidad':'Insalubre'}
        return res
    elif 201 <= calidad_aire <= 300:
        res = {'res':'La calidad aire del Aire muy poco saludable. Advertencias sanitarias de condiciones de emergencia. Es más probable que toda la población se vea afectada. Los niños y adultos activos y las personas con enfermedades respiratorias, como asma, deben evitar todo esfuerzo al aire libre; todos los demás, especialmente los niños, deben limitar el esfuerzo al aire libre.', 'calidad':'Dañino'}
        return res
    elif 301 <= calidad_aire:
        res = {'res':'La calidad aire del Aire es peligroso. Alerta de salud: todos pueden experimentar efectos de salud más graves. Todo el mundo debería evitar todo esfuerzo al aire libre.', 'calidad': 'Muy Dañino'}
        return res
    

@csrf_exempt
def recibir_ubicacion(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    
    else:
        ubicacion = request.POST.get('city')
        calidad_aire1 = obtener_calidad_aire(ubicacion, token_aqi)
        respuesta_ai = calidad_aire1['res']
        data = list(calidad_aire1.values())
        print(calidad_aire1)
        return JsonResponse({'res':calidad_aire1})
        
        #return JsonResponse({'error': 'Método no permitido'}, status=405)