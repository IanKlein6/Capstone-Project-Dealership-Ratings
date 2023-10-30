from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2

class CarModelAdmin(admin.ModelAdmin):
    list_display = ['car_make', 'name', 'type_car', 'year']
    list_filter = ['type_car', 'car_make', 'year']
    search_fields = ['car_make__name', 'name']

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
