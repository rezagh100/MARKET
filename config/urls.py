from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include('accounts.urls')),
    path("api/", include('products.urls')),
    path("api/", include('sellers.urls')),
    path("api/", include("offers.urls")),
    path("api/", include("orders.urls")),
    
]
