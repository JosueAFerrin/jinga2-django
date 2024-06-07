from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
import csv
from django.http import HttpResponse

productos = []

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'listar.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')
        
        producto = Producto(nombre=nombre, precio=precio, cantidad=cantidad)
        producto.save()
        
        return redirect('listar_productos')
    
    return render(request, 'crear.html')

def actualizar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.precio = request.POST.get('precio')
        producto.cantidad = request.POST.get('cantidad')
        producto.save()
        return redirect('listar_productos')
    
    return render(request, 'actualizar.html', {'producto': producto})

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    
    return render(request, 'eliminar.html', {'producto': producto})

def importar_productos(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']
        reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
        next(reader)  # Omitir el encabezado si existe
        errores = []
        
        for index, row in enumerate(reader):
            try:
                nombre = row[0]
                precio = row[1]
                cantidad = row[2]
                
                # Validar que el precio y la cantidad sean números válidos
                precio = float(precio)
                cantidad = int(cantidad)
                
                Producto.objects.create(nombre=nombre, precio=precio, cantidad=cantidad)
            except ValueError as e:
                errores.append(f"Error en la línea {index + 2}: {e}")
            except Exception as e:
                errores.append(f"Error en la línea {index + 2}: {e}")
        
        if errores:
            return render(request, 'importar.html', {'errores': errores})
        
        return redirect('listar_productos')
    
    return render(request, 'importar.html')


def exportar_productos(request):
    productos = Producto.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'
    writer = csv.writer(response)
    
    # Escribir el encabezado del CSV
    writer.writerow(['Nombre', 'Precio', 'Cantidad'])

    
    # Escribir los datos de los productos
    for producto in productos:
        writer.writerow([producto.nombre, producto.precio, producto.cantidad])
    
    return response