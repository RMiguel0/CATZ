from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
import requests, os
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def home(request):
    return render(request, 'home.html', {'ubicacion':'Hola', 'calidad_aire': 'chao', 'respuesta_ai': 'xd'} )


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


def profile(request):
    return render(request, 'profile.html')


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



token_aqi = "a9fa736d75e0f33dc4a9ba18292eab99fa46eb4d"
def obtener_calidad_aire(ciudad, token_aqi):
    base_url = "https://api.waqi.info/feed/"
    url = f"{base_url}{ciudad}/?token={token_aqi}"
    dic = {}

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get("status") == "ok":
            calidad_aire = data["data"]["aqi"]
            print(f"La calidad_aire del aire en {ciudad} es: {calidad_aire}")

            # Ahora, enviamos la calidad_aire del aire a OpenAI para obtener una respuesta_ai
            respuesta_ai = enviarCalidadAirea(calidad_aire)
            print(respuesta_ai)
            dic['aqi'] = calidad_aire
            dic['res'] = respuesta_ai
            return dic

        else:
            print("No se pudo obtener la información de calidad_aire del aire.")
            return JsonResponse({'error': 'No se pudo obtener la información de calidad_aire del aire.'})

    except Exception as e:
        print(f"Hubo un error al obtener la información: {e}")
        return JsonResponse({'error': f'Hubo un error al obtener la información: {e}'})



def enviarCalidadAirea(calidad_aire):
    if 0 <= calidad_aire <= 50:
        res = 'La calidad_aire del Aire es Buena, no se anticipan impactos a la salud cuando la calidad_aire del aire se encuentra en este intervalo.'
        return res
    elif 51 <= calidad_aire <= 100:
        res = 'La calidad_aire del Aire es Moderada, La calidad_aire del aire es aceptable; sin embargo,' 
        'para algunos contaminantes puede haber un problema de salud moderado para un número muy pequeño de personas que son inusualmente sensibles a la contaminación del aire.'
        'Los niños y adultos activos y las personas con enfermedades respiratorias, como asma, deben limitar el esfuerzo prolongado al aire libre.'
        return res
    elif 101 <= calidad_aire <= 150:
        res = 'La calidad_aire del Aire No es saludable para grupos sensibles.'
        'Los miembros de grupos sensibles pueden experimentar efectos sobre la salud. No es probable que el público en general se vea afectado.'
        'Los niños y adultos activos y las personas con enfermedades respiratorias, como asma, deben limitar el esfuerzo prolongado al aire libre.'
        return res
    
    elif 151 <= calidad_aire <= 200:
        res = {'respesta': '''
               La calidad_aire del Aire es insalubre.Todo el mundo puede empezar a experimentar efectos sobre la salud; 
               Los miembros de grupos sensibles pueden experimentar efectos más graves para la salud. Los niños y adultos activos y las personas con enfermedades respiratorias, 
               como asma, deben evitar el esfuerzo prolongado al aire libre; 
               todos los demás, especialmente los niños, deben limitar el esfuerzo prolongado al aire libre.
               '''
        }
        return res['respuesta_ai']
    
    elif 201 <= calidad_aire <= 300:
        res = 'La calidad_aire del Aire muy poco saludable'
        'Advertencias sanitarias de condiciones de emergencia. Es más probable que toda la población se vea afectada.'
        'Los niños y adultos activos y las personas con enfermedades respiratorias, como asma, deben evitar todo esfuerzo al aire libre;' 
        'todos los demás, especialmente los niños, deben limitar el esfuerzo al aire libre.'
        return res
    elif 301 <= calidad_aire:
        res = 'La calidad_aire del Aire es peligroso'
        'Alerta de salud: todos pueden experimentar efectos de salud más graves'
        'Todo el mundo debería evitar todo esfuerzo al aire libre.'
        return res
    

@csrf_exempt
def recibir_ubicacion(request):
    if request.method == 'POST':
        ubicacion = request.POST.get('city')
        calidad_aire1 = obtener_calidad_aire(ubicacion, token_aqi)
        calidad_aire = calidad_aire1['aqi']
        print(calidad_aire)
        respuesta_ai = calidad_aire1['res']
        print(respuesta_ai)
        return render(request, 'home.html', {
            'ubicacion':ubicacion,
            'calidad_aire': calidad_aire,
            'respuesta_ai': respuesta_ai
            }
        )
    else:
        return render(request, 'home.html')
        #return JsonResponse({'error': 'Método no permitido'}, status=405)
