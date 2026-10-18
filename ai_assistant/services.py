from offers.models import Offer


def get_recommendations(budget):
    return (
        Offer.objects
        .filter(stock__gt=0, price__lte=budget)
        .select_related('product', 'seller')
        .order_by('price')
    )
