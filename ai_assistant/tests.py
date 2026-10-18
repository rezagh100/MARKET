
from django.test import TestCase
from django.contrib.auth import get_user_model

from products.models import Category, Product
from sellers.models import SellerProfile
from offers.models import Offer

from ai_assistant.services import get_recommendations
from rest_framework.test import APIClient


User = get_user_model()


class RecommendationServiceTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic products",
        )

        self.user1 = User.objects.create_user(
            username="seller1",
            password="testpass123",
            phone_number="09120000001",
        )

        self.user2 = User.objects.create_user(
            username="seller2",
            password="testpass123",
            phone_number="09120000002",
        )

        self.seller1 = SellerProfile.objects.create(
            user=self.user1,
            store_name="Store One",
            description="First test store",
        )

        self.seller2 = SellerProfile.objects.create(
            user=self.user2,
            store_name="Store Two",
            description="Second test store",
        )

        self.product1 = Product.objects.create(
            title="Laptop A",
            description="Test laptop A",
            category=self.category,
        )

        self.product2 = Product.objects.create(
            title="Laptop B",
            description="Test laptop B",
            category=self.category,
        )

        Offer.objects.create(
            seller=self.seller1,
            product=self.product1,
            price=200000,
            stock=3,
        )

        Offer.objects.create(
            seller=self.seller2,
            product=self.product2,
            price=100000,
            stock=2,
        )

        Offer.objects.create(
            seller=self.seller1,
            product=self.product2,
            price=150000,
            stock=0,
        )

        Offer.objects.create(
            seller=self.seller2,
            product=self.product1,
            price=500000,
            stock=2,
        )

    def test_returns_only_available_offers_within_budget(self):
        recommendations = get_recommendations(budget=300000)

        self.assertEqual(recommendations.count(), 2)

        prices = list(
            recommendations.values_list("price", flat=True)
        )

        self.assertEqual(prices, [100000, 200000])
        
    
    def test_returns_empty_queryset_when_no_offer_matches_budget(self):
        recommendations = get_recommendations(budget=50000)

        self.assertEqual(recommendations.count(), 0)

    def test_includes_offer_when_price_equals_budget(self):
        recommendations = get_recommendations(budget=100000)

        self.assertEqual(recommendations.count(), 1)
        self.assertEqual(recommendations.first().price, 100000)
        
    
    def test_recommendation_api_returns_valid_results(self):
        client = APIClient()

        response = client.get(
            "/api/recommendations/",
            {"budget": 300000},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        prices = [item["price"] for item in response.data]
        self.assertEqual(prices, ["100000.00", "200000.00"])

        for item in response.data:
            self.assertGreater(item["stock"], 0)
            self.assertLessEqual(
                float(item["price"]),
                300000,
            )

    def test_recommendation_api_rejects_invalid_budget(self):
        client = APIClient()

        response = client.get(
            "/api/recommendations/",
            {"budget": "abc"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    
    def test_recommendation_api_requires_budget(self):
        client = APIClient()

        response = client.get("/api/recommendations/")

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_recommendation_api_rejects_zero_budget(self):
        client = APIClient()

        response = client.get(
            "/api/recommendations/",
            {"budget": 0},
        )

        self.assertEqual(response.status_code, 400)

    def test_recommendation_api_rejects_negative_budget(self):
        client = APIClient()

        response = client.get(
            "/api/recommendations/",
            {"budget": -100},
        )

        self.assertEqual(response.status_code, 400)

    def test_recommendation_api_returns_empty_list_when_no_match(self):
        client = APIClient()

        response = client.get(
            "/api/recommendations/",
            {"budget": 50000},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

