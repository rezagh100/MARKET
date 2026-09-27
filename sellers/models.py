from django.db import models
from accounts.models import User


class SellerProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.user.username