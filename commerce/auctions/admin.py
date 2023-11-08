from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Auction_Listings,Bids,Categories, Commenst

class CustomUserAdmin(UserAdmin):
    # Customize the list display, filter options, search fields, etc.
    list_display = ('username', 'email', 'first_name', 'last_name')

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Auction_Listings)
admin.site.register(Bids)
admin.site.register(Categories)
admin.site.register(Commenst)