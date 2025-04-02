from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'comuna', 'is_staff', 'is_active')  # 👈 añadimos comuna
    list_filter = ('is_staff', 'is_active', 'date_joined', 'comuna')  # 👈 añadimos comuna
    search_fields = ('email', 'first_name', 'last_name', 'comuna')  # 👈 añadimos comuna
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'comuna', 'profile_picture', 'resume')  # 👈 añadimos comuna
        }),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'comuna',  # 👈 añadimos comuna aquí también
                'password1', 'password2', 'is_staff', 'is_active'
            ),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
