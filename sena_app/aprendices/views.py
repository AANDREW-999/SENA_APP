from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Aprendiz
from instructores.models import Instructor
from .forms import AprendizForm

# Vista de inicio simple

def inicio(request):
    template = loader.get_template('inicio.html')
    mis_aprendices = Aprendiz.objects.order_by('-id')[:10]
    instructores_recientes = Instructor.objects.order_by('-id')[:10]
    context = {'mis_aprendices': mis_aprendices, 'instructores_recientes': instructores_recientes}
    return HttpResponse(template.render(context, request))

# Listado
class AprendizListView(ListView):
    model = Aprendiz
    template_name = 'lista_aprendices.html'
    context_object_name = 'mis_aprendices'
    paginate_by = 10

# Detalle
class AprendizDetailView(DetailView):
    model = Aprendiz
    template_name = 'aprendiz_detail.html'

# Crear
class AprendizCreateView(CreateView):
    model = Aprendiz
    form_class = AprendizForm
    template_name = 'aprendiz_form.html'
    success_url = reverse_lazy('lista_aprendices')

# Actualizar
class AprendizUpdateView(UpdateView):
    model = Aprendiz
    form_class = AprendizForm
    template_name = 'aprendiz_form.html'
    success_url = reverse_lazy('lista_aprendices')

# Eliminar
class AprendizDeleteView(DeleteView):
    model = Aprendiz
    template_name = 'aprendiz_confirm_delete.html'
    success_url = reverse_lazy('lista_aprendices')
