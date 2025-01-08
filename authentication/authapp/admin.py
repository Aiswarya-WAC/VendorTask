from django.contrib import admin

from authapp.models import Customer, Vendor

# Register your models here.

admin.site.register(Vendor)
admin.site.register(Customer)