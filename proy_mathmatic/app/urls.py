# cursos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path('', views.home, name='home'),
    
    # Cursos
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('cursos/<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    
    # Profesores
    path('profesores/', views.lista_profesores, name='lista_profesores'),
    path('profesores/<int:profesor_id>/', views.detalle_profesor, name='detalle_profesor'),
    
    # Estudiantes
    path('estudiantes/', views.lista_estudiantes, name='lista_estudiantes'),
    path('estudiantes/<int:estudiante_id>/', views.detalle_estudiante, name='detalle_estudiante'),
    path('registro-estudiante/', views.registro_estudiante, name='registro_estudiante'),
    
    # Órdenes/Matrículas
    path('ordenes/', views.lista_ordenes, name='lista_ordenes'),
    path('ordenes/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    path('crear-matricula/', views.crear_orden, name='crear_orden'),
    
    # Horarios
    path('horarios/', views.horarios_disponibles, name='horarios_disponibles'),
    
    # API endpoints
    path('api/horarios-por-dia/', views.get_horarios_por_dia, name='horarios_por_dia'),
]