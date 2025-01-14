
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('marca/<int:marca_id>/', views.zapatos_por_marca, name='zapatos_por_marca'),
    path('zapato/<int:zapato_id>/',views.detalle_zapato, name='detalle_zapato'),
    path('listaZapatilla/',views.listado_zapato, name='listado_zapato'),
    path('nuevaZapatilla/',views.nuevo_zapato, name='nuevo_zapato'),
    path('modificarZapatilla/<id>/',views.modificar_zapato, name='modificar_zapato'),
    path('eliminarZapatilla/<id>/',views.eliminar_zapato, name='eliminar_zapato'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)