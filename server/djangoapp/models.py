from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `
class CarMake(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
        

# <HINT> Create a Car Model model `
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dealer_id = models.IntegerField()
    
    TYPE_CHOICES = [
        ('SEDAN', 'Sedan'), 
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]
    type_car = models.CharField(max_length=50, choices=TYPE_CHOICES, default='SEDAN')
    year = models.DateField()

    def __str__ (self):
        return self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
