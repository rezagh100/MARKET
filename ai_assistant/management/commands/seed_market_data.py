
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from products.models import Category, Product
from sellers.models import SellerProfile
from offers.models import Offer

class Command(BaseCommand):
    help = "Create Persian demo data for the MARKET project"

    def handle(self, *args, **options):
        User = get_user_model()

        # 1. Categories
        categories_data = [
            ("موبایل و تبلت", "گوشی موبایل و لوازم مرتبط"),
            ("لپ‌تاپ و کامپیوتر", "کامپیوتر و تجهیزات جانبی"),
            ("صوتی و تصویری", "هدفون، اسپیکر و نمایشگر"),
            ("لوازم خانگی", "وسایل کاربردی خانه"),
            ("لوازم جانبی", "لوازم جانبی دیجیتال"),
        ]

        categories = {}

        for name, description in categories_data:
            category, _ = Category.objects.get_or_create(
                name=name,
                defaults={"description": description},
            )
            categories[name] = category

        # 2. Users and seller profiles
        sellers_data = [
            ("market_seller_01", "علی", "محمدی", "فروشگاه دیجیتال تهران"),
            ("market_seller_02", "سارا", "احمدی", "فروشگاه همراه پلاس"),
            ("market_seller_03", "رضا", "کریمی", "مرکز کالای دیجیتال"),
            ("market_seller_04", "مریم", "حسینی", "فروشگاه خانه مدرن"),
            ("market_seller_05", "امیر", "رضایی", "تک‌استور ایرانی"),
            ("market_seller_06", "نگار", "مرادی", "فروشگاه آوا"),
            ("market_seller_07", "محمد", "جعفری", "دیجیتال مارکت"),
            ("market_seller_08", "فاطمه", "کاظمی", "فروشگاه انتخاب"),
        ]

        sellers = {}

        for index, (username, first_name, last_name, store_name) in enumerate(
            sellers_data, start=1
        ):
            user = User.objects.filter(username=username).first()

            if user is None:
                user = User.objects.create_user(
                    username=username,
                    password="MarketDemo2026!",
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=f"099900000{index:02d}",
                )

            seller, _ = SellerProfile.objects.get_or_create(
                user=user,
                defaults={
                    "store_name": store_name,
                    "description": f"{store_name}؛ فروشنده محصولات منتخب",
                },
            )

            sellers[username] = seller

        # 3. Products
        products_data = [
            (
                "گوشی سامسونگ A55",
                "موبایل و تبلت",
                "گوشی میان‌رده سامسونگ با حافظه مناسب",
            ),
            (
                "گوشی شیائومی Redmi Note 13",
                "موبایل و تبلت",
                "گوشی اقتصادی با نمایشگر باکیفیت",
            ),
            (
                "گوشی آیفون ۱۳",
                "موبایل و تبلت",
                "گوشی اپل با حافظه ۱۲۸ گیگابایت",
            ),
            (
                "لپ‌تاپ لنوو IdeaPad",
                "لپ‌تاپ و کامپیوتر",
                "لپ‌تاپ مناسب برنامه‌نویسی و کارهای روزمره",
            ),
            (
                "لپ‌تاپ ایسوس VivoBook",
                "لپ‌تاپ و کامپیوتر",
                "لپ‌تاپ سبک برای کار و تحصیل",
            ),
            (
                "مانیتور ال‌جی ۲۴ اینچ",
                "صوتی و تصویری",
                "مانیتور مناسب کارهای اداری و برنامه‌نویسی",
            ),
            (
                "هدفون بلوتوثی انکر",
                "صوتی و تصویری",
                "هدفون بی‌سیم برای موسیقی و تماس",
            ),
            (
                "اسپیکر بلوتوثی جی‌بی‌ال",
                "صوتی و تصویری",
                "اسپیکر قابل حمل با صدای قدرتمند",
            ),
            (
                "پاوربانک ۲۰۰۰۰ میلی‌آمپر",
                "لوازم جانبی",
                "پاوربانک مناسب استفاده روزمره",
            ),
            (
                "جاروبرقی پاناسونیک",
                "لوازم خانگی",
                "جاروبرقی خانگی با قدرت مکش مناسب",
            ),
        ]

        products = {}

        for title, category_name, description in products_data:
            product, _ = Product.objects.get_or_create(
                title=title,
                category=categories[category_name],
                defaults={"description": description},
            )
            products[title] = product

        # 4. Offers: (product title, seller username, price in toman, stock)
        offers_data = [
            ("گوشی سامسونگ A55", "market_seller_01", 25000000, 5),
            ("گوشی سامسونگ A55", "market_seller_02", 26500000, 8),

            ("گوشی شیائومی Redmi Note 13", "market_seller_03", 12000000, 10),
            ("گوشی شیائومی Redmi Note 13", "market_seller_04", 11500000, 4),

            ("گوشی آیفون ۱۳", "market_seller_01", 38000000, 3),
            ("گوشی آیفون ۱۳", "market_seller_05", 39500000, 2),

            ("لپ‌تاپ لنوو IdeaPad", "market_seller_02", 39000000, 4),
            ("لپ‌تاپ لنوو IdeaPad", "market_seller_06", 42000000, 3),

            ("لپ‌تاپ ایسوس VivoBook", "market_seller_03", 45000000, 2),
            ("لپ‌تاپ ایسوس VivoBook", "market_seller_07", 43500000, 5),

            ("مانیتور ال‌جی ۲۴ اینچ", "market_seller_04", 8500000, 6),
            ("مانیتور ال‌جی ۲۴ اینچ", "market_seller_08", 9000000, 4),

            ("هدفون بلوتوثی انکر", "market_seller_05", 3200000, 12),
            ("هدفون بلوتوثی انکر", "market_seller_06", 3500000, 7),

            ("اسپیکر بلوتوثی جی‌بی‌ال", "market_seller_07", 6500000, 5),
            ("اسپیکر بلوتوثی جی‌بی‌ال", "market_seller_08", 6200000, 3),

            ("پاوربانک ۲۰۰۰۰ میلی‌آمپر", "market_seller_01", 1800000, 15),
            ("پاوربانک ۲۰۰۰۰ میلی‌آمپر", "market_seller_04", 1950000, 0),

            ("جاروبرقی پاناسونیک", "market_seller_02", 12500000, 3),
            ("جاروبرقی پاناسونیک", "market_seller_07", 13000000, 6),
        ]

        for title, username, price, stock in offers_data:
            Offer.objects.get_or_create(
                seller=sellers[username],
                product=products[title],
                defaults={
                    "price": price,
                    "stock": stock,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data created successfully: "
                f"{Category.objects.filter(name__in=[x[0] for x in categories_data]).count()} categories, "
                f"{len(products)} products, "
                f"{len(sellers)} sellers, "
                f"{Offer.objects.filter(product__in=products.values()).count()} offers."
            )
        )

        self.stdout.write(
            "Demo users password: MarketDemo2026! (development only)"
        )
