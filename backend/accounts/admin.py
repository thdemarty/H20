from django.contrib.auth.admin import UserAdmin
from .models import Patient, Utilisateur
from django.contrib import admin

admin.site.register(Patient)
admin.site.register(Utilisateur, UserAdmin)