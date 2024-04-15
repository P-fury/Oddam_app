from django.contrib import admin

from oddam_app.models import Institution
from user.models import CustomUser
from django.contrib.auth.admin import UserAdmin


# Register your models here.

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Institution)
