from django.contrib import admin
from .models import Food,Order, Payment
# Register your models here.

admin.site.register(Food)
admin.site.register(Order)
admin.site.register(Payment)
