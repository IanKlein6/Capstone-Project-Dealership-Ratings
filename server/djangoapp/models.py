from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `

class CarMake(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


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
        raise NotImplementedError)
    year = models.DateField()

    def __str__ (self):


# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
