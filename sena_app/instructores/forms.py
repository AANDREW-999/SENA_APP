from django import forms
from .models import Instructor

class DateInput(forms.DateInput):
    input_type = 'date'

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['documento_identidad','tipo_documento','nombre','apellido','telefono','correo','fecha_nacimiento','ciudad','direccion','nivel_educativo','especialidad','anos_experiencia','activo','fecha_vinculacion']
        widgets = {
            'documento_identidad': forms.TextInput(attrs={
                'required': True,
                'pattern': r'\d{6,20}',
                'inputmode': 'numeric',
                'placeholder': 'Documento de identidad',
                'class': 'form-control'
            }),
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'required': True,'placeholder': 'Nombre','class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'required': True,'placeholder': 'Apellido','class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'pattern': r'\d{7,10}','inputmode': 'numeric','placeholder': 'Teléfono','class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'required': True,'placeholder': 'Correo electrónico','class': 'form-control'}),
            'fecha_nacimiento': DateInput(attrs={'required': True,'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'placeholder': 'Ciudad','class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'rows': 2,'placeholder': 'Dirección','class': 'form-control'}),
            'nivel_educativo': forms.Select(attrs={'class': 'form-select'}),
            'especialidad': forms.TextInput(attrs={'required': True,'placeholder': 'Especialidad','class': 'form-control'}),
            'anos_experiencia': forms.NumberInput(attrs={'required': True,'min': 0,'max': 60,'step': 1,'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fecha_vinculacion': DateInput(attrs={'required': True,'class': 'form-control'}),
        }
        help_texts = {
            'documento_identidad': 'Sólo números (6 a 20 dígitos)'.strip(),
            'telefono': 'Número fijo o celular (7 a 10 dígitos)'.strip(),
            'correo': 'Usa un correo válido (se verifica unicidad)'.strip(),
            'anos_experiencia': 'Años completos de experiencia'.strip(),
        }

