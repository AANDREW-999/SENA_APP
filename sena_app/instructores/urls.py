from django.urls import path
from . import views

urlpatterns = [
    path('', views.instructores, name='lista_instructores'),
    path('nuevo/', views.InstructorCreateView.as_view(), name='instructor_create'),
    path('<int:id_instructor>/', views.detalle_instructor, name='detalle_instructor'),
    path('<int:pk>/editar/', views.InstructorUpdateView.as_view(), name='instructor_update'),
    path('<int:pk>/eliminar/', views.InstructorDeleteView.as_view(), name='instructor_delete'),
]
