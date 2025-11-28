from django.db import models

class Aprendiz(models.Model):
    documento_identidad = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    ciudad = models.CharField(max_length=100)
    programa = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.documento_identidad}"
# Create your models here.
