from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy

from .models import Product, Review
from .models import Category
from .models import Tag

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Review)
#admin.site.unregister(TokenProxy)