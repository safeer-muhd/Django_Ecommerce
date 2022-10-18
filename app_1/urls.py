from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('collection',views.collection,name='collection'),
    path('collections/<str:name>',views.collectionsview,name='collections'),
    path('collections/<str:cname>/<str:pname>',views.product_details,name='product_details'),
    path('addtocart',views.add_to_cart,name='addtocart'),
    path('cart',views.cart_page,name='cart'),
    path('remove_cart',views.remove_cart,name='remove_cart'),
    path('favorite',views.fav_page,name='favorite'),
    path('checkout',views.checkout_page,name='checkout')
]
