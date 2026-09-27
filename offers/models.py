from django.db import models

from products.models import Product
from sellers.models import SellerProfile


class Offer(models.Model):
    seller = models.ForeignKey(
        SellerProfile,
        on_delete=models.CASCADE,
        related_name='offers'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT,
        related_name='offers'
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['seller', 'product'],
                name='unique_seller_product_offer'
            )
        ]

    def __str__(self):
        return f"{self.seller.store_name} - {self.product.title}"