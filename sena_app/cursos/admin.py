from django.contrib import admin
from .models import Curso, AprendizCurso, InstructorCurso

admin.site.register(Curso)
admin.site.register(AprendizCurso)
admin.site.register(InstructorCurso)
# Register your models here.
