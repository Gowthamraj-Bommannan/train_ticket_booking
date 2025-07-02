from django.db import models
import random

class Station(models.Model):
    """
    Represents a railway station with a unique code and name.

    Fields:
        code (str): Unique short code for the station (e.g., 'MAS' for Chennai Central).
        name (str): Full name of the station (e.g., 'Chennai Central').
        is_active (bool): Marks whether the station is active or not.
        created_at (datetime): Timestamp when the station was created.
        updated_at (datetime): Timestamp when the station was last updated.
    """

    code = models.CharField(max_length= 10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        db_table = 'station'
        verbose_name = 'Station'
        verbose_name_plural = 'Stations'
    
class Train(models.Model):
    """
    Represents a train available for reservation.

    Fields:
        number (str): Unique train number (e.g., '12345').
        name (str): Name of the train (e.g., 'Chennai Express').
        compartments (int): Number of compartments in the train (default is 10).
        seats_per_compartment (int): Number of seats per compartment (default is 10).
        is_active (bool): Flag to enable/disable a train.
        created_at (datetime): Timestamp when the train was added.
        updated_at (datetime): Timestamp when the train was last updated.

    Properties:
        total_seats (int): Total seats = compartments * seats_per_compartment.
    """

    number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    from_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='departing_trains')
    to_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='arriving_trains')
    compartments = models.PositiveIntegerField(default=5)
    seats_per_compartment = models.PositiveBigIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_seats(self):
        return self.compartments * self.seats_per_compartment
    
    class Meta:
        db_table = 'train'
        verbose_name = 'Train'
        verbose_name_plural = 'Trains'
    
    def generate_train_number(self):
        while True:
            number = f"{random.randint(10000, 99999)}"
            if not Train.objects.filter(number=number).exists():
                return number
            
    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.generate_train_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number} - {self.name}"
    
class TrainStation(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, 
                              related_name='train_stations')
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    stop_number = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['stop_number']
        db_table = 'train_station'
        verbose_name = 'Train Station'
        verbose_name_plural = 'Train Stations'

    def __str__(self):
        return f"{self.train.number} - {self.station.code} - {self.stop_number}"
    