from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Instructor
from .forms import InstructorForm


def instructores(request):
    qs = Instructor.objects.all().order_by('-id')
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'instructores': page_obj.object_list,
        'page_obj': page_obj,
        'total_instructores': qs.count(),
    }
    return render(request, 'lista_instructores.html', context)


def detalle_instructor(request, id_instructor):
    instructor = get_object_or_404(Instructor, id=id_instructor)
    context = {'instructor': instructor}
    return render(request, 'detalle_instructor.html', context)


class InstructorCreateView(CreateView):
    model = Instructor
    form_class = InstructorForm
    template_name = 'instructor_form.html'
    success_url = reverse_lazy('lista_instructores')


class InstructorUpdateView(UpdateView):
    model = Instructor
    form_class = InstructorForm
    template_name = 'instructor_form.html'
    success_url = reverse_lazy('lista_instructores')


class InstructorDeleteView(DeleteView):
    model = Instructor
    template_name = 'instructor_confirm_delete.html'
    success_url = reverse_lazy('lista_instructores')
