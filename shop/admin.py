from django.contrib import admin
from .models import Item,Profile,Category,Cart,Seller
# Register your models here.
admin.site.site_title='Duka Discount admin'
admin.site.site_header = "Duka Discount Administration Panel"

admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Seller)
