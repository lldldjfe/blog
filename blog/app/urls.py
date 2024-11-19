from django.urls import path
from .views import *

urlpatterns = [
   path('', index),
   path('about', about),
   path('contacts',contacts) ,
   path("reg",reg),
   path("auth",auth),
   path('logout',logout),
   path('add_blog', add_blog),
   path('view/<int:id>', view_new),
   path('add_like/<int:id_new>', add_like),
   path('catalog', catalog),
   path('catalog/<int:id>', catalog_detail),
   path('add_cart/<int:id_product>', add_cart),
   path('cart', cart),
   path('delete_product', delete_product),
   path('add_order', add_order)
]
