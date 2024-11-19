from django.contrib import admin
from .models import User, Blog, Comment, Product, Category, Order

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)