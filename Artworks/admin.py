from django.contrib import admin
from Artworks.models import Artwork, Cart, CartItem, Order, MpesaPayment

# Register your models here.
admin.site.register(Artwork)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(MpesaPayment)

