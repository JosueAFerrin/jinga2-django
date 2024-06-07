from django.urls import path
from . import views

urlpatterns = [
    # URLs de vistas normales
    path('', views.listar_productos, name='listar_productos'),
    path('crear/', views.crear_producto, name='crear_productos'),
    path('actualizar/<int:id>/', views.actualizar_producto, name='actualizar_productos'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_productos'),
    path('importar/', views.importar_productos, name='importar_productos'),
    path('exportar/', views.exportar_productos, name='exportar_productos')
]