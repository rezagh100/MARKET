from django.db import transaction

from offers.models import Offer
from orders.models import Order, OrderItem


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
                    raise serializer.V("Not enough stock.")

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

            return order