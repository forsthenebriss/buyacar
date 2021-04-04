from django.contrib import admin
from rango.models import UserProfile, Car

admin.site.register(UserProfile)

#class that lists attributes in given order
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'model', 'price', 'seller')
    
#show us the Page and Category in the admin login
admin.site.register(Car, CarAdmin)
