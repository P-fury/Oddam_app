from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

from oddam_app.models import Institution
from user.models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# admin.site.register(CustomUser, UserAdmin)
admin.site.register(Institution)


class CustomUserAdmin(UserAdmin):
    def has_delete_permission(self, request, obj=None):
        admins_count = CustomUser.objects.filter(is_superuser=True).count()
        if obj is not None and obj == request.user:
            return False
        if admins_count < 2:
            return False
        return super().has_delete_permission(request, obj)


admin.site.register(CustomUser, CustomUserAdmin)
