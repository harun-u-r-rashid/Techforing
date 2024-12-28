from django.contrib import admin

from .models import User, OneTimePassword


class UserAdmin(admin.ModelAdmin):
        list_display = ['id', 'username', 'email']

admin.site.register(User, UserAdmin)
admin.site.register(OneTimePassword)

