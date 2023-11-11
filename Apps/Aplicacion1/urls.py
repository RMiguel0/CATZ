from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.recibir_ubicacion, name='home'),
    path('login/', views.signup, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.singout, name='singout'),
    path('clima/', views.clima, name='aire'),
    path('watch/', views.recibir_ubicacion, name='home1'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)