from django.test import TestCase, Client
from django.urls import reverse
from aprendices.models import Aprendiz
from django.db import IntegrityError

class AprendizTestBase(TestCase):
    
    def setUp(self):
        self.aprendiz = Aprendiz.objects.create(
            documento_identidad="123456789",
            nombre="Nixon",
            apellido="Zapata",
            telefono="1234567890",
            correo="nixon@example.com",
            fecha_nacimiento="1990-01-01",
            ciudad="Bogotá",
            programa="Analisis y Desarrollo de Software",
        )
        self.client = Client()

class AprendizModelTest(AprendizTestBase):
    
    # 1. Verificar creación correcta
    def test_aprendiz_se_crea_correctamente(self):
        self.assertEqual(self.aprendiz.documento_identidad, "123456789")
        self.assertEqual(self.aprendiz.nombre, "Nixon")
        self.assertEqual(self.aprendiz.apellido, "Zapata")
        self.assertEqual(self.aprendiz.telefono, "1234567890")
        self.assertEqual(self.aprendiz.correo, "nixon@example.com")
        self.assertEqual(self.aprendiz.fecha_nacimiento, "1990-01-01")
        self.assertEqual(self.aprendiz.ciudad, "Bogotá")
        self.assertEqual(self.aprendiz.programa, "Analisis y Desarrollo de Software")

    # 2. Verificar método __str__
    def test_str_retorna_nombre_completo_y_documento(self):
        self.assertEqual(str(self.aprendiz), "Nixon Zapata - 123456789")

    # 3. Verificar campos opcionales aceptan null
    def test_campos_opcionales_aceptan_null(self):
        aprendiz = Aprendiz.objects.create(
            documento_identidad="987654321",
            nombre="María",
            apellido="Gómez",
            telefono=None,
            correo="maria@example.com",
            fecha_nacimiento=None,
            ciudad="Duitama",
            programa="Diseño Gráfico"
        )
        self.assertIsNone(aprendiz.telefono)
        self.assertIsNone(aprendiz.fecha_nacimiento)

    # 4. Verificar unicidad de documento_identidad
    def test_documento_identidad_es_unico(self):
        with self.assertRaises(IntegrityError):
            Aprendiz.objects.create(
                documento_identidad="123456789",
                nombre="Juan",
                apellido="Pérez",
                telefono="9876543210",
                correo="juan@example.com",
                fecha_nacimiento="1995-05-05",
                ciudad="Medellín",
                programa="Ingeniería"
            )

    # 5. Verificar unicidad de correo
    def test_correo_es_unico(self):
        with self.assertRaises(IntegrityError):
            Aprendiz.objects.create(
                documento_identidad="987654321",
                nombre="Ana",
                apellido="López",
                telefono="9876543210",
                correo="nixon@example.com",
                fecha_nacimiento="1995-05-05",
                ciudad="Cali",
                programa="Diseño"
            )

    # 6. Verificar longitud máxima de documento_identidad
    def test_documento_identidad_longitud_maxima(self):
        aprendiz = Aprendiz.objects.create(
            documento_identidad="1" * 50,
            nombre="Carlos",
            apellido="Martínez",
            telefono="1234567890",
            correo="carlos@example.com",
            fecha_nacimiento="1992-02-02",
            ciudad="Cartagena",
            programa="Arquitectura"
        )
        self.assertEqual(len(aprendiz.documento_identidad), 50)

    # 7. Verificar longitud máxima de nombre
    def test_nombre_longitud_maxima(self):
        aprendiz = Aprendiz.objects.create(
            documento_identidad="987654322",
            nombre="A" * 100,
            apellido="López",
            telefono="1234567890",
            correo="ana@example.com",
            fecha_nacimiento="1995-05-05",
            ciudad="Cali",
            programa="Diseño"
        )
        self.assertEqual(len(aprendiz.nombre), 100)

    # 8. Verificar longitud máxima de apellido
    def test_apellido_longitud_maxima(self):
        aprendiz = Aprendiz.objects.create(
            documento_identidad="987654323",
            nombre="Ana",
            apellido="L" * 100,
            telefono="1234567890",
            correo="ana2@example.com",
            fecha_nacimiento="1995-05-05",
            ciudad="Cali",
            programa="Diseño"
        )
        self.assertEqual(len(aprendiz.apellido), 100)

    # 9. Verificar longitud máxima de teléfono
    def test_telefono_longitud_maxima(self):
        aprendiz = Aprendiz.objects.create(
            documento_identidad="987654324",
            nombre="Ana",
            apellido="López",
            telefono="1" * 20,
            correo="ana3@example.com",
            fecha_nacimiento="1995-05-05",
            ciudad="Cali",
            programa="Diseño"
        )
        self.assertEqual(len(aprendiz.telefono), 20)

    # 10. Verificar longitud máxima de ciudad
    def test_ciudad_longitud_maxima(self):
        aprendiz = Aprendiz.objects.create(
            documento_identidad="987654325",
            nombre="Ana",
            apellido="López",
            telefono="1234567890",
            correo="ana4@example.com",
            fecha_nacimiento="1995-05-05",
            ciudad="C" * 100,
            programa="Diseño"
        )
        self.assertEqual(len(aprendiz.ciudad), 100)

    # 11. Verificar longitud máxima de programa
    def test_programa_longitud_maxima(self):
        aprendiz = Aprendiz.objects.create(
            documento_identidad="987654326",
            nombre="Ana",
            apellido="López",
            telefono="1234567890",
            correo="ana5@example.com",
            fecha_nacimiento="1995-05-05",
            ciudad="Cali",
            programa="P" * 150
        )
        self.assertEqual(len(aprendiz.programa), 150)

    # 12. Verificar creación sin teléfono
    def test_creacion_sin_telefono(self):
        aprendiz = Aprendiz.objects.create(
            documento_identidad="987654327",
            nombre="Ana",
            apellido="López",
            telefono=None,
            correo="ana6@example.com",
            fecha_nacimiento="1995-05-05",
            ciudad="Cali",
            programa="Diseño"
        )
        self.assertIsNone(aprendiz.telefono)

    # 13. Verificar creación sin fecha de nacimiento
    def test_creacion_sin_fecha_nacimiento(self):
        aprendiz = Aprendiz.objects.create(
            documento_identidad="987654328",
            nombre="Ana",
            apellido="López",
            telefono="1234567890",
            correo="ana7@example.com",
            fecha_nacimiento=None,
            ciudad="Cali",
            programa="Diseño"
        )
        self.assertIsNone(aprendiz.fecha_nacimiento)

    # 14. Verificar ordenamiento por apellido y nombre
    def test_ordenamiento_por_apellido_y_nombre(self):
        Aprendiz.objects.all().delete()  # Limpiar aprendices creados en setUp
        aprendiz1 = Aprendiz.objects.create(
            documento_identidad="987654329",
            nombre="Carlos",
            apellido="Zapata",
            telefono="1234567890",
            correo="carlos@example.com",
            fecha_nacimiento="1995-05-05",
            ciudad="Cali",
            programa="Diseño"
        )
        aprendiz2 = Aprendiz.objects.create(
            documento_identidad="987654330",
            nombre="Ana",
            apellido="López",
            telefono="1234567890",
            correo="ana8@example.com",
            fecha_nacimiento="1995-05-05",
            ciudad="Cali",
            programa="Diseño"
        )
        aprendices = list(Aprendiz.objects.all())
        self.assertEqual(aprendices, [aprendiz2, aprendiz1])
# Continúa con más pruebas...