from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from .models import Carrito, ElementoCarrito
from home.models import zapato 
from .forms import AñadirAlCarritoForm, EliminarDelCarritoForm


def ver_carrito(request):
    carrito = Carrito.objects.first()
    if not carrito:
        carrito = Carrito.objects.create()
    elementos = ElementoCarrito.objects.filter(carrito=carrito)
    return render(request, 'carrito/ver_carrito.html', {'carrito': carrito, 'elementos': elementos})

def añadir_al_carrito(request):
    if request.method == 'POST':
        form = AñadirAlCarritoForm(request.POST)
        if form.is_valid():
            zapato_id = form.cleaned_data['zapato_id']
            cantidad = form.cleaned_data['cantidad']
            zapato_obj = get_object_or_404(zapato, id=zapato_id)
            carrito = Carrito.objects.first()
            if not carrito:
                carrito = Carrito.objects.create()
            elemento, created = ElementoCarrito.objects.get_or_create(carrito=carrito, zapato=zapato_obj)
            if not created:
                elemento.cantidad += cantidad
            else:
                elemento.cantidad = cantidad
            elemento.save()
            return redirect('ver_carrito')
    return redirect('home')

def actualizar_cantidad(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        elemento_id = data.get('elemento_id')
        action = data.get('action')
        elemento = get_object_or_404(ElementoCarrito, id=elemento_id)
        
        if action == 'incrementar':
            elemento.cantidad += 1
        elif action == 'decrementar' and elemento.cantidad > 1:
            elemento.cantidad -= 1
        
        elemento.save()

        carrito = elemento.carrito
        carrito.total = sum(e.precio_total for e in carrito.elementocarrito_set.all())
        carrito.save()

        response = {
            'cantidad': elemento.cantidad,
            'precio_total': str(elemento.precio_total),
            'total': str(carrito.total)
        }
        return JsonResponse(response)

def eliminar_del_carrito(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        elemento_id = data.get('elemento_id')
        elemento = get_object_or_404(ElementoCarrito, id=elemento_id)
        elemento.delete()

        carrito = elemento.carrito
        carrito.total = sum(e.precio_total for e in carrito.elementocarrito_set.all())
        carrito.save()

        response = {
            'total': str(carrito.total)
        }
        return JsonResponse(response)