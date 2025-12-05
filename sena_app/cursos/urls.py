from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('nuevo/', views.crear_curso, name='crear_curso'),
    path('<int:curso_id>/editar/', views.editar_curso, name='editar_curso'),
    path('<int:curso_id>/eliminar/', views.eliminar_curso, name='eliminar_curso'),
    # Listas relacionales
    path('aprendices-curso/', views.lista_aprendices_curso, name='lista_aprendices_curso'),
    path('instructores-curso/', views.lista_instructores_curso, name='lista_instructores_curso'),
    # CRUD AprendizCurso
    path('aprendices-curso/nuevo/', views.crear_aprendiz_curso, name='crear_aprendiz_curso'),
    path('aprendices-curso/<int:pk>/', views.detalle_aprendiz_curso, name='detalle_aprendiz_curso'),
    path('aprendices-curso/<int:pk>/editar/', views.editar_aprendiz_curso, name='editar_aprendiz_curso'),
    path('aprendices-curso/<int:pk>/eliminar/', views.eliminar_aprendiz_curso, name='eliminar_aprendiz_curso'),
    # CRUD InstructorCurso
    path('instructores-curso/nuevo/', views.crear_instructor_curso, name='crear_instructor_curso'),
    path('instructores-curso/<int:pk>/', views.detalle_instructor_curso, name='detalle_instructor_curso'),
    path('instructores-curso/<int:pk>/editar/', views.editar_instructor_curso, name='editar_instructor_curso'),
    path('instructores-curso/<int:pk>/eliminar/', views.eliminar_instructor_curso, name='eliminar_instructor_curso'),
]
