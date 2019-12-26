from django.db import models

# Create your models here.
class TempSensor(models.Model):
    """simple temperature sensor for monitoring"""
    description = models.CharField(max_length=1024, default="Not - Defined")
    name = models.CharField(max_length=256)
    last_temperature = models.FloatField(default=0.0)
    hw_id = models.CharField(max_length=256, default='Not_Defined')

    def __str__(self):
        return self.name