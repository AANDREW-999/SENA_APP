from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('aprendices/', views.AprendizListView.as_view(), name='lista_aprendices'),
    path('aprendices/nuevo/', views.AprendizCreateView.as_view(), name='aprendiz_create'),
    path('aprendices/<int:pk>/', views.AprendizDetailView.as_view(), name='aprendiz_detail'),
    path('aprendices/<int:pk>/editar/', views.AprendizUpdateView.as_view(), name='aprendiz_update'),
    path('aprendices/<int:pk>/eliminar/', views.AprendizDeleteView.as_view(), name='aprendiz_delete'),
]