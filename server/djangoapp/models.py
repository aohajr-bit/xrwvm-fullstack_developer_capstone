from django.db import models


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    # Used by your admin.py list_display
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"

    CAR_TYPE_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon"),
    ]

    # Many CarModels belong to one CarMake
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")

    # Required by the lab (dealer in Cloudant)
    dealer_id = models.IntegerField()

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    year = models.IntegerField()

    # Used by your admin.py list_display
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
