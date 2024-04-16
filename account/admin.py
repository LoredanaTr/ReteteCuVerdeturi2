from django.contrib import admin
from account.models import WishlistItem


# Register your models here.
@admin.register(WishlistItem)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']