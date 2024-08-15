from django.contrib import admin

# Register your models here.
from .models import User, Film

admin.site.register(User)
admin.site.register(Film)