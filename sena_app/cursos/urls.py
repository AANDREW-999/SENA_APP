from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('nuevo/', views.crear_curso, name='crear_curso'),
    path('<int:curso_id>/editar/', views.editar_curso, name='editar_curso'),
    path('<int:curso_id>/eliminar/', views.eliminar_curso, name='eliminar_curso'),
    # Nuevas listas relacionales
    path('aprendices-curso/', views.lista_aprendices_curso, name='lista_aprendices_curso'),
    path('instructores-curso/', views.lista_instructores_curso, name='lista_instructores_curso'),
]
