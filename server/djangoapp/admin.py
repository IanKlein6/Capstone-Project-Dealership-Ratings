from django.contrib import admin
from .models import CarMake, CarModel



# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['car_make', 'name', 'type_car', 'year']  # Use field names that exist in CarModel
    list_filter = ['type_car', 'car_make', 'year']  # Use field names that exist in CarModel
    search_fields = ['car_make__name', 'name']  # Use double underscores to access related fields


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
