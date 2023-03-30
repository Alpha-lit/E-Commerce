from django.urls import path, include
from .views import *
urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('', Home, name="home"),
    path('product/<int:id>', ProductDetails, name="product_details"),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-confirmation/', order_confirmation, name="order_confirmation"),
    path('profile/', profile, name="profil"),
]

