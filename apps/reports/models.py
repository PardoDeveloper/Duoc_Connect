from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AnonymousReport(models.Model):
    CATEGORY_CHOICES = [
        ('acoso', 'Acoso'),
        ('discriminacion', 'Discriminación'),
        ('fraude', 'Fraude'),
        ('otro', 'Otro'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_category_display()} - {self.submitted_at.date()}"

class Reporte(models.Model):
    TIPO_CHOICES = [
        ('equipo_danado', 'Equipo dañado'),
        ('acoso', 'Acoso'),
        ('bullying', 'Bullying'),
        ('reclamo', 'Reclamo'),
        ('coordinacion', 'Contacto con coordinación')
    ]

    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    laboratorio = models.CharField(max_length=100, blank=True, null=True)
    evidencia = models.FileField(upload_to='evidencias/', null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo.title()} - {self.fecha.strftime('%Y-%m-%d')}"

# admin.py para que aparezca en el panel de administración
from django.contrib import admin
from .models import Reporte

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'fecha', 'usuario', 'laboratorio')
    search_fields = ('tipo', 'descripcion', 'laboratorio', 'usuario__email')
    list_filter = ('tipo', 'fecha')