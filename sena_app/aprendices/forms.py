from django import forms
from .models import Aprendiz

class DateInput(forms.DateInput):
    input_type = 'date'

class AprendizForm(forms.ModelForm):
    class Meta:
        model = Aprendiz
        fields = ['documento_identidad','nombre','apellido','telefono','correo','fecha_nacimiento','ciudad','programa']
        widgets = {
            'documento_identidad': forms.TextInput(attrs={
                'required': True,
                'pattern': r'\d{10}',
                'maxlength': '10',
                'minlength': '10',
                'inputmode': 'numeric',
                'placeholder': 'Documento (10 dígitos)',
                'class': 'form-control'
            }),
            'nombre': forms.TextInput(attrs={'required': True,'placeholder': 'Nombre','class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'required': True,'placeholder': 'Apellido','class': 'form-control'}),
            'telefono': forms.TextInput(attrs={
                'pattern': r'\d{10}',
                'maxlength': '10',
                'minlength': '10',
                'inputmode': 'numeric',
                'placeholder': 'Teléfono (10 dígitos)',
                'class': 'form-control'
            }),
            # Sin validación HTML5 de email (usa input text)
            'correo': forms.TextInput(attrs={'placeholder': 'Correo','class': 'form-control'}),
            'fecha_nacimiento': DateInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'placeholder': 'Ciudad','class': 'form-control'}),
            'programa': forms.TextInput(attrs={'placeholder': 'Programa','class': 'form-control'}),
        }
        help_texts = {
            'documento_identidad': 'Exactamente 10 dígitos numéricos.',
            'telefono': 'Exactamente 10 dígitos numéricos (opcional).',
        }

    def clean_documento_identidad(self):
        val = (self.cleaned_data.get('documento_identidad') or '').strip()
        if not val.isdigit() or len(val) != 10:
            raise forms.ValidationError('El documento debe tener exactamente 10 dígitos numéricos.')
        return val

    def clean_telefono(self):
        val = (self.cleaned_data.get('telefono') or '').strip()
        if val:
            if not val.isdigit() or len(val) != 10:
                raise forms.ValidationError('El teléfono debe tener exactamente 10 dígitos numéricos.')
        return val

