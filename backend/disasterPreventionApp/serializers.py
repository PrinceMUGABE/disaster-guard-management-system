from rest_framework import serializers
from userApp.models import CustomUser
from disasterPredictionApp.models import DisasterPrediction
from .models import PreventionStrategy


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'email', 'role', 'created_at']


# Prediction Serializer
class PredictionSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()  # Nested serializer to include user details

    class Meta:
        model = DisasterPrediction
        fields = [
            'id',
            'district',
            'sector',
            'temperature',
            'wind_speed',
            'humidity',
            'rainfall',
            'soil_type',
            'risk_level',
            'confidence_score',
            'most_likely_disaster',
            'created_at',
            'created_by',
        ]
        
        
# Prevention Strategy Serializer
class PreventionStrategySerializer(serializers.ModelSerializer):
    prediction = PredictionSerializer(read_only=True)
    human_resources = serializers.SerializerMethodField()
    equipment_resources = serializers.SerializerMethodField()
    implementation_timeline = serializers.JSONField()
    
    def get_human_resources(self, obj):
        if obj.resource_requirements and 'personnel' in obj.resource_requirements:
            return obj.resource_requirements['personnel']
        return None
    
    def get_equipment_resources(self, obj):
        if obj.resource_requirements and 'equipment' in obj.resource_requirements:
            return obj.resource_requirements['equipment']
        return None
    
    class Meta:
        model = PreventionStrategy
        fields = [
            'id',
            'prediction',
            'action',
            'description',
            'priority',
            'responsible_entity',
            'timeframe',
            'current_conditions',
            'risk_assessment',
            'implementation_timeline',
            'human_resources',
            'equipment_resources',
            'budget',
            'status',  # Added the status field here
            'created_at',
        ]