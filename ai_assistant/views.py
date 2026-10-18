
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .services import get_recommendations
from .serializers import RecommendationSerializer


class RecommendViewSet(ViewSet):

    def list(self, request):
        budget = request.query_params.get('budget')

        if budget is None:
            return Response(
                {'error': 'The budget parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            budget = int(budget)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Budget must be a valid integer.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if budget <= 0:
            return Response(
                {'error': 'Budget must be greater than zero.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        recommendations = get_recommendations(budget)

        serializer = RecommendationSerializer(
            [
                {
                    'product': offer.product.title,
                    'seller': offer.seller.store_name,
                    'price': offer.price,
                    'stock': offer.stock,
                }
                for offer in recommendations
            ],
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
