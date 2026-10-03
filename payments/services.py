from django.db import transaction
from orders.models import Order
from .models import Payment


class PaymentService:
    def create_payment(self, order):
        payment = Payment.objects.create(
            order=order, amount=order.total_price, status=Payment.PaymentStatus.PENDING)
        return payment

    def pay(self, payment):
        with transaction.atomic():
            if payment.status == Payment.PaymentStatus.PENDING:
                payment.status = Payment.PaymentStatus.PAID
                payment.order.status = Order.OrderStatus.PAID
                payment.order.save()
                payment.save()
                return True
            
            return False
