from django.db import models
from django.conf import settings

class DisasterPrediction(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    district = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    temperature = models.CharField(max_length=50)
    wind_speed = models.CharField(max_length=50)
    humidity = models.CharField(max_length=50)
    rainfall = models.CharField(max_length=50)
    soil_type = models.CharField(max_length=100)
    risk_level = models.CharField(max_length=50)
    confidence_score = models.CharField(max_length=50)
    most_likely_disaster = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.district}, {self.sector} - {self.most_likely_disaster}"
