from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import *
from datetime import date

def home(request):
    """Vista principal de la academia"""
    cursos_disponibles = Cursos.objects.filter(
        iddisponibilidadcurso__disponibilidad=True
    ).select_related('idprofesor', 'iddisponibilidadcurso')
    
    context = {
        'cursos': cursos_disponibles,
        'total_cursos': cursos_disponibles.count(),
    }
    return render(request, 'app/home.html', context)

def lista_cursos(request):
    """Vista para mostrar todos los cursos disponibles"""
    search_query = request.GET.get('search', '')
    
    cursos = Cursos.objects.filter(
        iddisponibilidadcurso__disponibilidad=True
    ).select_related('idprofesor')
    
    if search_query:
        cursos = cursos.filter(
            Q(nombrecurso__icontains=search_query) |
            Q(idprofesor__nombres__icontains=search_query) |
            Q(idprofesor__apellidopaterno__icontains=search_query)
        )
    
    context = {
        'cursos': cursos,
        'search_query': search_query,
    }
    return render(request, 'app/lista_cursos.html', context)

def detalle_curso(request, curso_id):
    """Vista para mostrar el detalle de un curso específico"""
    curso = get_object_or_404(Cursos, idcurso=curso_id)
    
    # Obtener horarios disponibles para este curso
    horarios_disponibles = Horario.objects.filter(
        iddisponibilidadhorario__disponibilidad=True
    ).select_related('iddia')
    
    # Obtener salones disponibles
    salones_disponibles = Salones.objects.filter(
        iddisponibilidad__disponibilidad=True
    )
    
    context = {
        'curso': curso,
        'horarios': horarios_disponibles,
        'salones': salones_disponibles,
    }
    return render(request, 'app/detalle_curso.html', context)

def lista_profesores(request):
    """Vista para mostrar todos los profesores"""
    profesores = Profesores.objects.all()
    
    context = {
        'profesores': profesores,
    }
    return render(request, 'app/lista_profesores.html', context)

def detalle_profesor(request, profesor_id):
    """Vista para mostrar el detalle de un profesor y sus cursos"""
    profesor = get_object_or_404(Profesores, idprofesor=profesor_id)
    
    # Cursos que imparte el profesor
    cursos_profesor = Cursos.objects.filter(
        idprofesor=profesor,
        iddisponibilidadcurso__disponibilidad=True
    )
    
    context = {
        'profesor': profesor,
        'cursos': cursos_profesor,
    }
    return render(request, 'app/detalle_profesor.html', context)

def registro_estudiante(request):
    """Vista para registrar un nuevo estudiante"""
    if request.method == 'POST':
        # Obtener datos del formulario
        nombres = request.POST.get('nombres')
        apellido_paterno = request.POST.get('apellido_paterno')
        apellido_materno = request.POST.get('apellido_materno')
        telefono = request.POST.get('telefono')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        
        try:
            # Crear nuevo estudiante
            estudiante = Estudiantes.objects.create(
                nombres=nombres,
                apellidopaterno=apellido_paterno,
                apellidomaterno=apellido_materno,
                telefonoestudiante=telefono,
                fechanacimiento=fecha_nacimiento,
                email=email,
                direccion=direccion
            )
            
            messages.success(request, 'Estudiante registrado exitosamente!')
            return redirect('detalle_estudiante', estudiante_id=estudiante.idestudiante)
            
        except Exception as e:
            messages.error(request, f'Error al registrar estudiante: {str(e)}')
    
    return render(request, 'app/registro_estudiante.html')

def lista_estudiantes(request):
    """Vista para mostrar todos los estudiantes"""
    search_query = request.GET.get('search', '')
    
    estudiantes = Estudiantes.objects.all()
    
    if search_query:
        estudiantes = estudiantes.filter(
            Q(nombres__icontains=search_query) |
            Q(apellidopaterno__icontains=search_query) |
            Q(apellidomaterno__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    context = {
        'estudiantes': estudiantes,
        'search_query': search_query,
    }
    return render(request, 'app/lista_estudiantes.html', context)

def detalle_estudiante(request, estudiante_id):
    """Vista para mostrar el detalle de un estudiante"""
    estudiante = get_object_or_404(Estudiantes, idestudiante=estudiante_id)
    
    # Órdenes del estudiante
    ordenes = Orden.objects.filter(
        idestudiante=estudiante
    ).select_related('idcurso', 'idsalon', 'idhorario')
    
    context = {
        'estudiante': estudiante,
        'ordenes': ordenes,
    }
    return render(request, 'app/detalle_estudiante.html', context)

def crear_orden(request):
    """Vista para crear una nueva orden de matrícula"""
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id')
        curso_id = request.POST.get('curso_id')
        salon_id = request.POST.get('salon_id')
        horario_id = request.POST.get('horario_id')
        
        try:
            # Verificar que todos los elementos existan y estén disponibles
            estudiante = get_object_or_404(Estudiantes, idestudiante=estudiante_id)
            curso = get_object_or_404(Cursos, idcurso=curso_id)
            salon = get_object_or_404(Salones, idsalon=salon_id)
            horario = get_object_or_404(Horario, idhorario=horario_id)
            
            # Verificar disponibilidad
            if not curso.iddisponibilidadcurso.disponibilidad:
                messages.error(request, 'El curso no está disponible')
                return redirect('crear_orden')
            
            if not salon.iddisponibilidad.disponibilidad:
                messages.error(request, 'El salón no está disponible')
                return redirect('crear_orden')
            
            if not horario.iddisponibilidadhorario.disponibilidad:
                messages.error(request, 'El horario no está disponible')
                return redirect('crear_orden')
            
            # Crear la orden
            orden = Orden.objects.create(
                fechaorden=date.today(),
                idestudiante=estudiante,
                idcurso=curso,
                idsalon=salon,
                idhorario=horario,
                estado=True
            )
            
            messages.success(request, 'Matrícula realizada exitosamente!')
            return redirect('detalle_orden', orden_id=orden.idorden)
            
        except Exception as e:
            messages.error(request, f'Error al crear la matrícula: {str(e)}')
    
    # Obtener datos para el formulario
    estudiantes = Estudiantes.objects.all()
    cursos = Cursos.objects.filter(iddisponibilidadcurso__disponibilidad=True)
    salones = Salones.objects.filter(iddisponibilidad__disponibilidad=True)
    horarios = Horario.objects.filter(iddisponibilidadhorario__disponibilidad=True)
    
    context = {
        'estudiantes': estudiantes,
        'cursos': cursos,
        'salones': salones,
        'horarios': horarios,
    }
    return render(request, 'app/crear_orden.html', context)

def detalle_orden(request, orden_id):
    """Vista para mostrar el detalle de una orden"""
    orden = get_object_or_404(Orden, idorden=orden_id)
    
    context = {
        'orden': orden,
    }
    return render(request, 'app/detalle_orden.html', context)

def lista_ordenes(request):
    """Vista para mostrar todas las órdenes"""
    search_query = request.GET.get('search', '')
    
    ordenes = Orden.objects.all().select_related(
        'idestudiante', 'idcurso', 'idsalon', 'idhorario'
    )
    
    if search_query:
        ordenes = ordenes.filter(
            Q(idestudiante__nombres__icontains=search_query) |
            Q(idestudiante__apellidopaterno__icontains=search_query) |
            Q(idcurso__nombrecurso__icontains=search_query)
        )
    
    context = {
        'ordenes': ordenes,
        'search_query': search_query,
    }
    return render(request, 'app/lista_ordenes.html', context)

def horarios_disponibles(request):
    """Vista para mostrar horarios disponibles por día"""
    horarios = Horario.objects.filter(
        iddisponibilidadhorario__disponibilidad=True
    ).select_related('iddia').order_by('iddia__nombredia', 'horainicio')
    
    context = {
        'horarios': horarios,
    }
    return render(request, 'app/horarios_disponibles.html', context)

# Vista AJAX para obtener horarios por día
def get_horarios_por_dia(request):
    """API para obtener horarios disponibles por día"""
    dia_id = request.GET.get('dia_id')
    
    if dia_id:
        horarios = Horario.objects.filter(
            iddia_id=dia_id,
            iddisponibilidadhorario__disponibilidad=True
        ).values('idhorario', 'descripcion', 'horainicio', 'horafin')
        
        return JsonResponse({'horarios': list(horarios)})
    
    return JsonResponse({'horarios': []})