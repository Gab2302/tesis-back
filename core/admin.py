from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, PatientNutritionist, Scan, Task, Recipe, ScanRecipeSuggestion, ProgressLog

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'role', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('name', 'role', 'nutritionist_code')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ['email']
    filter_horizontal = ('groups', 'user_permissions',)

# Registro de modelos
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(PatientNutritionist)
admin.site.register(Scan)
admin.site.register(Task)
admin.site.register(Recipe)
admin.site.register(ScanRecipeSuggestion)
admin.site.register(ProgressLog)

