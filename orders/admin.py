from django.contrib import admin
from .models import Order,OrderItem

admin.site.register(OrderItem)
admin.site.register(Order)