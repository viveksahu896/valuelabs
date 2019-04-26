from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ProductPrice, GiftCard, Product


class ProductPriceView(APIView):

    def get(self, request, *args, **kwargs):
        date = request.GET.get('date')
        productCode = request.GET.get('productCode')
        giftCardCode = request.GET.get('giftCardCode')
        if not productCode:
            return Response({'Message': 'Please pass the product code'})
        if date:
            date = self.convert_date(date)
            day = date.day
            month = date.month
        else:
            day = None
            month = None
        # Filter based on product type
        product_price_filter_by_code = ProductPrice.objects.filter(product__code=productCode)
        # Filter for dates
        if month == 11 and day in [23, 24, 25]:
            product_price = product_price_filter_by_code.filter(price_schedule_from__day=day, price_schedule_from__month=month)
            price = product_price[0].special_price
        elif date and date >= self.convert_date('January 1, 2019') and month != 11 and day not in [23, 24, 25]:
            product_price = product_price_filter_by_code.filter(price_schedule_from__gte=date)
            price = product_price[0].special_price
        else:
            product = Product.objects.get(code=productCode)
            price = product.price/100
        if giftCardCode:
            price = self.price_after_discount(price, giftCardCode)
        if not price:
            price = 'FREE!'
        return Response({'productPrice': price})

    def convert_date(self, str):
        # Covert user input date to date object of Python
        return datetime.strptime(str, '%B %d, %Y').date()

    def price_after_discount(self, product_price, giftCardCode):
        # To apply the discount on price
        if product_price:
            giftCard = GiftCard.objects.get(code=giftCardCode)
            price = product_price - (giftCard.amount/100)
            return price
