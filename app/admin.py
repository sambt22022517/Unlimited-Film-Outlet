from django.contrib import admin

# Register your models here.
from .models import User, Film, Habit, Cart, Bill, BillItem

admin.site.register(User)
admin.site.register(Film)
admin.site.register(Habit)
admin.site.register(Cart)
admin.site.register(Bill)
admin.site.register(BillItem)