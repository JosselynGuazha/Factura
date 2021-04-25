from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cliente
from .forms import ClienteForm
from django.contrib import messages
from django.db.models import Q


# Create your views here.


def inicio(request):
    return render(request, 'principal/index.html', {})


@login_required
def factura(request):
    return render(request, 'principal/factura.html', {})


@login_required
def crearCliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente guardado con Exito')
            return redirect('crearCliente')
    else:
        form = ClienteForm()
    return render(request, 'principal/crearCliente.html', {'titulo': 'Crear Cliente', 'form': form})


@login_required
def buscarCliente(request):
    context = {}
    identificacionGet = request.GET.get("identificacion")
    tipoIdentificacionGet = request.GET.get("tipoIdentificacion")

    if identificacionGet and tipoIdentificacionGet:
        if tipoIdentificacionGet == 'TODOS':
            cliente = Cliente.objects.filter(identificacion = identificacionGet)
            cont = Cliente.objects.filter(identificacion = identificacionGet).count()
        else:
            cliente = Cliente.objects.filter(identificacion = identificacionGet, tipoIdentificacion = tipoIdentificacionGet)
            cont = Cliente.objects.filter(identificacion = identificacionGet, tipoIdentificacion = tipoIdentificacionGet).count()
        if cont == 0:
            context = {'message' : 'Cliente no existe'}
        else:
            context = {'data' : cliente}
    return render(request, 'principal/buscarCliente.html', context)


@login_required
def modificarCliente(request, id):    
    cliente = get_object_or_404(Cliente, id=id)
    print("Este valor", id )
    print("Este valor", cliente )

    if request.method == "POST":
            form = ClienteForm(request.POST, request.FILES, instance=cliente)
            if form.is_valid():
                cliente = form.save()
                cliente.save()
                messages.success(request, 'Cliente Modificado con Exito')
                return redirect('buscarCliente')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'principal/modificarCliente.html', {'form':form})
