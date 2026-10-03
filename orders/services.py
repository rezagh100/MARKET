from django.db import transaction

from offers.models import Offer
from orders.models import Order, OrderItem
from payments.services import PaymentService



class InsufficientStockError(Exception):
    pass


class OrderService:

    def create_order(self, user, items):
        with transaction.atomic():
            order = Order.objects.create(
                user=user
            )

            total_price = 0

            for item in items:
                offer = Offer.objects.select_for_update().get(
                    pk=item['offer'].pk
                )

                unit_price = offer.price

                if item['quantity'] > offer.stock:
                    raise InsufficientStockError(
                        "Not enough stock."
                    )

                offer.stock -= item['quantity']
                offer.save()

                OrderItem.objects.create(
                    order=order,
                    offer=offer,
                    quantity=item['quantity'],
                    unit_price=unit_price
                )

                total_price += (
                    unit_price * item['quantity']
                )

            order.total_price = total_price
            order.save()
            PaymentService().create_payment(order=order)
            return order

    def cancel_order(self, user, order):
        with transaction.atomic():

            if order.status == Order.OrderStatus.PENDING:

                for item in order.items.all():
                    offer = Offer.objects.select_for_update().get(
                        pk=item.offer.pk
                    )

                    offer.stock += item.quantity
                    offer.save()

                order.status = Order.OrderStatus.CANCELLED
                order.save()

                return True

            return False