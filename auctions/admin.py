from django.contrib import admin

from .models import auctions, Bids, Comments

# Register your models here.
admin.site.register(auctions)
admin.site.register(Bids)
admin.site.register(Comments)