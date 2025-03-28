from django.contrib import admin
from .models import AnonymousReport

@admin.register(AnonymousReport)
class AnonymousReportAdmin(admin.ModelAdmin):
    list_display = ('category', 'submitted_at', 'is_reviewed')
    list_filter = ('category', 'is_reviewed')
    ordering = ('-submitted_at',)
    readonly_fields = ('category', 'description', 'submitted_at')  # solo lectura
    actions = ['marcar_como_revisada', 'marcar_como_no_revisada']

    def marcar_como_revisada(self, request, queryset):
        updated = queryset.update(is_reviewed=True)
        self.message_user(request, f"{updated} denuncia(s) marcadas como revisadas.")

    def marcar_como_no_revisada(self, request, queryset):
        updated = queryset.update(is_reviewed=False)
        self.message_user(request, f"{updated} denuncia(s) marcadas como no revisadas.")

    marcar_como_revisada.short_description = "Marcar como revisada"
    marcar_como_no_revisada.short_description = "Marcar como no revisada"