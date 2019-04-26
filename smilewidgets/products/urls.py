from django.urls import path
from .views import ProductPriceView

app_name = "products"
urlpatterns = [
    path('get-price/', ProductPriceView.as_view()),
]