from django.contrib import admin
from .models import AnonymousReport

@admin.register(AnonymousReport)
class AnonymousReportAdmin(admin.ModelAdmin):
    list_display = ('category', 'submitted_at', 'is_reviewed')
    list_filter = ('category', 'is_reviewed')
    readonly_fields = ('description', 'submitted_at')
