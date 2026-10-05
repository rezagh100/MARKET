from django.db import models
from django.conf import settings


class SellerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.user.username
