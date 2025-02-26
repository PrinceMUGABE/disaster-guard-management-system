from django.db import models
from disasterPredictionApp.models import DisasterPrediction

# Create your models here.


from django.db import models

class PreventionStrategy(models.Model):
    STATUS_CHOICES = (
        ('waiting', 'Waiting'),
        ('pending', 'Pending'),
        ('finished', 'Finished'),
    )
    
    prediction = models.ForeignKey(DisasterPrediction, on_delete=models.CASCADE, related_name='strategies')
    action = models.CharField(max_length=500)
    description = models.TextField()
    priority = models.CharField(max_length=50)
    responsible_entity = models.CharField(max_length=100)
    timeframe = models.CharField(max_length=50)  # e.g., "immediate", "short_term", "long_term"
    current_conditions = models.JSONField(null=True, blank=True)  # Save conditions like temperature, rainfall, etc.
    risk_assessment = models.JSONField(null=True, blank=True)  # Save risk level and confidence score
    implementation_timeline = models.JSONField(null=True, blank=True)  # Save immediate, short-term, long-term dates
    resource_requirements = models.JSONField(null=True, blank=True)  # Save personnel, equipment, etc.
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # Save estimated budget
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')  # New status field
    created_at = models.DateTimeField(auto_now_add=True)
