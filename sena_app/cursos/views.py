from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from .models import Curso, AprendizCurso, InstructorCurso
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django import forms


# Formulario básico para Curso (similar a otros módulos)
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['codigo','nombre','programa','instructor_coordinador','instructores','fecha_inicio','fecha_fin','horario','aula','cupos_maximos','estado','observaciones']
        widgets = {
            'codigo': forms.TextInput(attrs={'class':'form-control','maxlength':'30','placeholder':'Código único'}),
            'nombre': forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del curso'}),
            'programa': forms.Select(attrs={'class':'form-select'}),
            'instructor_coordinador': forms.Select(attrs={'class':'form-select'}),
            'instructores': forms.SelectMultiple(attrs={'class':'form-select'}),
            'fecha_inicio': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'horario': forms.TextInput(attrs={'class':'form-control','placeholder':'Ej: Lun-Vie 7:00-12:00'}),
            'aula': forms.TextInput(attrs={'class':'form-control','placeholder':'Ambiente/Aula'}),
            'cupos_maximos': forms.NumberInput(attrs={'class':'form-control','min':'1'}),
            'estado': forms.Select(attrs={'class':'form-select'}),
            'observaciones': forms.Textarea(attrs={'class':'form-control','rows':3}),
        }

# Formularios para relaciones
class AprendizCursoForm(forms.ModelForm):
    class Meta:
        model = AprendizCurso
        fields = ['curso','aprendiz','estado','nota_final','observaciones']
        widgets = {
            'curso': forms.Select(attrs={'class':'form-select'}),
            'aprendiz': forms.Select(attrs={'class':'form-select'}),
            'estado': forms.Select(attrs={'class':'form-select'}),
            'nota_final': forms.NumberInput(attrs={'class':'form-control','step':'0.1','min':'0','max':'5'}),
            'observaciones': forms.Textarea(attrs={'class':'form-control','rows':3}),
        }

class InstructorCursoForm(forms.ModelForm):
    class Meta:
        model = InstructorCurso
        fields = ['curso','instructor','rol']
        widgets = {
            'curso': forms.Select(attrs={'class':'form-select'}),
            'instructor': forms.Select(attrs={'class':'form-select'}),
            'rol': forms.TextInput(attrs={'class':'form-control','placeholder':'Rol en el curso'}),
        }


# Lista
def lista_cursos(request):
    cursos = Curso.objects.all()
    # Construir opciones únicas para selects del template
    programas = []
    coordinadores = []
    estados = [
        {'value': code, 'label': label}
        for code, label in Curso.ESTADO_CHOICES
    ]
    prog_set = set()
    coord_set = set()
    for c in cursos:
        # Programa: mostrar "codigo - nombre" o nombre según tu tabla
        prog_label = str(c.programa)
        coord_label = str(c.instructor_coordinador)
        if prog_label and prog_label not in prog_set:
            prog_set.add(prog_label)
            programas.append(prog_label)
        if coord_label and coord_label not in coord_set:
            coord_set.add(coord_label)
            coordinadores.append(coord_label)
    return render(request, 'lista_cursos.html', {
        'lista_cursos': cursos,
        'total_cursos': cursos.count(),
        'programas': programas,
        'coordinadores': coordinadores,
        'estados': estados,
    })


# Detalle
def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    aprendices_curso = curso.aprendizcurso_set.all()
    instructores_curso = curso.instructorcurso_set.all()
    return render(request, 'detalle_curso.html', {
        'curso': curso,
        'aprendices_curso': aprendices_curso,
        'instructores_curso': instructores_curso,
    })


# Crear
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save()
            messages.success(request, 'Curso creado correctamente.')
            return redirect('detalle_curso', curso_id=curso.id)
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = CursoForm()
    return render(request, 'curso_form.html', {'form': form, 'modo':'crear'})


# Editar
def editar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            curso = form.save()
            messages.success(request, 'Curso actualizado correctamente.')
            return redirect('detalle_curso', curso_id=curso.id)
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'curso_form.html', {'form': form, 'modo':'editar', 'curso': curso})


# Eliminar
def eliminar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso eliminado correctamente.')
        return redirect('lista_cursos')
    return render(request, 'curso_confirm_delete.html', {'curso': curso})


# Nuevas vistas: listados relacionales

def lista_aprendices_curso(request):
    qs = AprendizCurso.objects.select_related('curso', 'aprendiz').all()
    programa_code = request.GET.get('programa', '').strip()
    curso_code = request.GET.get('curso', '').strip()
    if programa_code:
        qs = qs.filter(curso__programa__codigo__icontains=programa_code)
    if curso_code:
        qs = qs.filter(curso__codigo__icontains=curso_code)
    context = {
        'items': qs,
        'total': qs.count(),
        'programa_filter': programa_code,
        'curso_filter': curso_code,
    }
    return render(request, 'lista_aprendices_curso.html', context)


def lista_instructores_curso(request):
    qs = InstructorCurso.objects.select_related('curso', 'instructor').all()
    programa_code = request.GET.get('programa', '').strip()
    curso_code = request.GET.get('curso', '').strip()
    if programa_code:
        qs = qs.filter(curso__programa__codigo__icontains=programa_code)
    if curso_code:
        qs = qs.filter(curso__codigo__icontains=curso_code)
    context = {
        'items': qs,
        'total': qs.count(),
        'programa_filter': programa_code,
        'curso_filter': curso_code,
    }
    return render(request, 'lista_instructores_curso.html', context)


# CRUD AprendizCurso

def crear_aprendiz_curso(request):
    if request.method == 'POST':
        form = AprendizCursoForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, 'Aprendiz asignado al curso correctamente.')
            return redirect('detalle_aprendiz_curso', pk=obj.id)
        messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = AprendizCursoForm()
    return render(request, 'aprendiz_curso_form.html', {'form': form})


def editar_aprendiz_curso(request, pk):
    obj = get_object_or_404(AprendizCurso, pk=pk)
    if request.method == 'POST':
        form = AprendizCursoForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            messages.success(request, 'Registro actualizado correctamente.')
            return redirect('detalle_aprendiz_curso', pk=obj.id)
        messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = AprendizCursoForm(instance=obj)
    return render(request, 'aprendiz_curso_form.html', {'form': form, 'obj': obj})


def eliminar_aprendiz_curso(request, pk):
    obj = get_object_or_404(AprendizCurso, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Registro eliminado correctamente.')
        return redirect('lista_aprendices_curso')
    return render(request, 'aprendiz_curso_confirm_delete.html', {'obj': obj})


def detalle_aprendiz_curso(request, pk):
    obj = get_object_or_404(AprendizCurso, pk=pk)
    return render(request, 'aprendiz_curso_detail.html', {'obj': obj})


# CRUD InstructorCurso

def crear_instructor_curso(request):
    if request.method == 'POST':
        form = InstructorCursoForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, 'Instructor asignado al curso correctamente.')
            return redirect('detalle_instructor_curso', pk=obj.id)
        messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = InstructorCursoForm()
    return render(request, 'instructor_curso_form.html', {'form': form})


def editar_instructor_curso(request, pk):
    obj = get_object_or_404(InstructorCurso, pk=pk)
    if request.method == 'POST':
        form = InstructorCursoForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            messages.success(request, 'Registro actualizado correctamente.')
            return redirect('detalle_instructor_curso', pk=obj.id)
        messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = InstructorCursoForm(instance=obj)
    return render(request, 'instructor_curso_form.html', {'form': form, 'obj': obj})


def eliminar_instructor_curso(request, pk):
    obj = get_object_or_404(InstructorCurso, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Registro eliminado correctamente.')
        return redirect('lista_instructores_curso')
    return render(request, 'instructor_curso_confirm_delete.html', {'obj': obj})


def detalle_instructor_curso(request, pk):
    obj = get_object_or_404(InstructorCurso, pk=pk)
    return render(request, 'instructor_curso_detail.html', {'obj': obj})
# Create your views here.
