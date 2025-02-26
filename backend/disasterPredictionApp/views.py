from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from rest_framework.response import Response
from .models import DisasterPrediction
from disasterPreventionApp.models import PreventionStrategy
from django.utils import timezone
from datetime import timedelta

import joblib
import json
import joblib
import random
import pandas as pd
import numpy as np
import joblib
import json
import requests
from typing import Dict, Union
from disasterPreventionApp.utils import DisasterPreventionSystem
from disasterPreventionApp.models import PreventionStrategy
# Create your views here.

class DistrictNotFoundError(Exception):
    """Exception raised when a district is not found in Rwanda."""
    pass

class SectorNotFoundError(Exception):
    """Exception raised when a sector is not found in the specified district."""
    pass


def get_weather_data(location):
    api_key = "54bfe931d3e776f190416f2bd20819d3"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        
        # print(f"\n\nWEATHER DATA\n")
        # for key, value in data.items():
        #     print(f"{key}: {value}")
            
            
        temp_celsius = data['main']['temp'] - 273.15
        weather_info = {
            'temperature': round(temp_celsius, 2),
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'rainfall': data['rain']['1h'] if 'rain' in data and '1h' in data['rain'] else 0,
            'latitude': data['coord']['lat'],
            'longitude': data['coord']['lon']
        }
        
        print(f" Weather Info: {weather_info}")
        return weather_info
    else:
        print("\n Weather information not found from API\n")
        raise Exception(f"Could not find district in on the map: {response.status_code}")

def get_sector_soil_type(dataset, district_name, sector_name):
    """
    Retrieve the soil type for a specific district and sector.
    
    Parameters:
    dataset (pandas.DataFrame): DataFrame containing the Rwanda geographical data
    district_name (str): Name of the district
    sector_name (str): Name of the sector
    
    Returns:
    str: Soil type for the specified sector
        Raises DistrictNotFoundError if district is not found.
        Raises SectorNotFoundError if sector is not found in the district.
    """
    # Convert inputs to title case to match dataset format
    district_name = district_name.title()
    sector_name = sector_name.title()
    
    # Check if the district exists in the dataset
    if not any(dataset['district'].str.strip() == district_name):
        raise DistrictNotFoundError(f"The district '{district_name}' is not found in Rwanda.")
    
    # Filter the dataset for the specific district and sector
    result = dataset[
        (dataset['district'].str.strip() == district_name) & 
        (dataset['sector'].str.strip() == sector_name)
    ]
    
    # Check if the sector exists in the district
    if len(result) == 0:
        raise SectorNotFoundError(f"The sector '{sector_name}' is not found in the district '{district_name}'.")
        
    # Return the soil type
    return result['soil_type'].iloc[0]



def get_most_likely_disaster(prediction_data):
    """
    Determine the most likely disaster type based on environmental conditions
    and historical data.
    """
    disaster_scores = {
        'Flood': (
            prediction_data['flood_count_5yr'] * 2 +
            prediction_data['flash_flood_count_5yr'] * 1.5 +
            prediction_data['riverine_flood_count_5yr']
        ) * (1 + prediction_data['rainfall'] / 100 if 'rainfall' in prediction_data else 1),
        
        'Landslide': (
            prediction_data['landslide_count_5yr'] * 2 +
            prediction_data['mudslide_count_5yr']
        ) * (1 + prediction_data['rainfall'] / 100 if 'rainfall' in prediction_data else 1),
        
        'Storm': (
            prediction_data['severe_storm_count_5yr'] * 1.5 +
            prediction_data['windstorm_count_5yr'] +
            prediction_data['hailstorm_count_5yr'] +
            prediction_data['lightning_strike_count_5yr']
        ) * (1 + prediction_data['wind_speed'] / 10 if 'wind_speed' in prediction_data else 1),
        
        'Drought': prediction_data['drought_months_5yr'] * 2,
        
        'Forest Fire': prediction_data['forest_fire_count_5yr'] * (
            2 if prediction_data['soil_type'] == 'Sandy' else 1
        ),
        
        'Earthquake': prediction_data['earthquake_count_5yr'] * 3
    }
    
    # Check if disaster_scores is not empty
    if not disaster_scores:
        raise ValueError("Disaster scores are empty. Cannot determine disaster.")
    
    # Ensure the correct format
    most_likely_disaster = max(disaster_scores.items(), key=lambda x: x[1], default=(None, None))
    
    # Handle cases where there is no valid disaster
    if most_likely_disaster[0] is None:
        raise ValueError("Unable to determine the most likely disaster.")
    
    return most_likely_disaster[0]


def create_test_dataframe(single_row_dict):
    required_columns = [
        'district', 'sector', 'latitude', 'longitude', 'soil_type',
        'flood_count_5yr', 'flash_flood_count_5yr', 'riverine_flood_count_5yr',
        'landslide_count_5yr', 'mudslide_count_5yr', 'drought_months_5yr',
        'severe_storm_count_5yr', 'windstorm_count_5yr', 'hailstorm_count_5yr',
        'lightning_strike_count_5yr', 'earthquake_count_5yr', 'forest_fire_count_5yr',
        'epidemic_outbreak_count_5yr', 'casualties_5yr'
    ]
    
    # Create a complete data dictionary first
    data = {}
    for col in required_columns:
        if col in single_row_dict:
            value = single_row_dict[col]
            if col in ['latitude', 'longitude']:
                value = float(value)
            elif col in ['district', 'sector', 'soil_type']:
                value = str(value)
            else:
                value = int(value)
        else:
            value = 0 if col not in ['district', 'sector', 'soil_type'] else ''
        data[col] = [value]
    
    # Create DataFrame at once
    return pd.DataFrame(data)
 
    
    
  
rwanda_sectors_dataset_infor = pd.read_csv('geographic demograph/rwanda_geographical_demographic_sectors.csv')

def load_and_test_model(single_row_dict):
    """
    Load and run the prediction model with proper error handling and risk level mapping.
    
    Args:
        single_row_dict: Dictionary containing the input features
        
    Returns:
        tuple: (risk_level, confidence_score)
    """
    try:
        # Load model and scaler
        loaded_model = joblib.load('historical disaster/Gradient Boosting_model.pkl')
        scaler = joblib.load('historical disaster/scaler.pkl')
        
        # Load feature metadata
        with open('historical disaster/metadata.json', 'r') as f:
            metadata = json.load(f)
        
        # Create test dataframe
        test_data = create_test_dataframe(single_row_dict)
        
        # Calculate total disasters
        disaster_columns = [col for col in test_data.columns if '_count_5yr' in col]
        test_data['total_disasters'] = test_data[disaster_columns].sum(axis=1)
        
        # Get dummy variables
        categorical_columns = ['district', 'sector', 'soil_type']
        test_data_encoded = pd.get_dummies(test_data, columns=categorical_columns)
        
        # Ensure all expected columns are present
        expected_columns = metadata['feature_columns']
        missing_columns = set(expected_columns) - set(test_data_encoded.columns)
        
        if missing_columns:
            additional_columns = pd.DataFrame(0, 
                                        index=test_data_encoded.index,
                                        columns=list(missing_columns))
            test_data_encoded = pd.concat([test_data_encoded, additional_columns], axis=1)
        
        # Reorder columns to match expected order
        test_data_encoded = test_data_encoded[expected_columns]
        
        # Scale numerical features
        numerical_cols = [col for col in test_data_encoded.columns 
                        if not any(col.startswith(f"{cat}_") for cat in categorical_columns)]
        test_data_encoded[numerical_cols] = scaler.transform(test_data_encoded[numerical_cols])
        
        # Make prediction
        prediction_proba = loaded_model.predict_proba(test_data_encoded)[0]
        max_prob = max(prediction_proba)
        
        # Map prediction probability to risk level
        if max_prob >= 0.7:
            return 'High', round(max_prob * 100, 2)
        elif max_prob >= 0.4:
            return 'Medium', round(max_prob * 100, 2)
        else:
            return 'Low', round(max_prob * 100, 2)
            
    except Exception as e:
        print(f"Error in model prediction: {str(e)}")
        return 'Medium', 50.0  # Default to Medium risk with 50% confidence if there's an error

def predict_disaster_risk(location: str, sector: str, weather_data: Dict) -> Dict[str, str]:
    """
    Predict disaster risk and return both risk level and most likely disaster.
    
    Args:
        location: District name
        sector: Sector name
        weather_data: Dictionary containing weather information
        
    Returns:
        Dictionary containing risk level, confidence score, and most likely disaster
    """
    prediction_data = {
        'district': location,
        'sector': sector,
        'latitude': weather_data['latitude'],
        'longitude': weather_data['longitude'],
        'soil_type': get_sector_soil_type(rwanda_sectors_dataset_infor, location, sector),
        'flood_count_5yr': min(5, int(weather_data['rainfall'] * 2)) if 'rainfall' in weather_data else random.randint(0, 2),
        'flash_flood_count_5yr': min(3, int(weather_data['rainfall'] * 1.5)) if 'rainfall' in weather_data else random.randint(0, 1),
        'riverine_flood_count_5yr': min(2, int(weather_data['rainfall'])) if 'rainfall' in weather_data else random.randint(0, 1),
        'landslide_count_5yr': random.randint(0, 2),
        'mudslide_count_5yr': random.randint(0, 2),
        'drought_months_5yr': random.randint(0, 12),
        'severe_storm_count_5yr': random.randint(0, 3),
        'windstorm_count_5yr': min(5, int(weather_data['wind_speed'])) if 'wind_speed' in weather_data else random.randint(0, 2),
        'hailstorm_count_5yr': random.randint(0, 2),
        'lightning_strike_count_5yr': random.randint(0, 3),
        'earthquake_count_5yr': random.randint(0, 1),
        'forest_fire_count_5yr': random.randint(0, 1),
        'epidemic_outbreak_count_5yr': random.randint(0, 1),
        'casualties_5yr': random.randint(0, 10)
    }
    
    # Get the model prediction for risk level and confidence score
    risk_level, confidence_score = load_and_test_model(prediction_data)
    
    # Get the most likely disaster type based on conditions
    most_likely_disaster = get_most_likely_disaster(prediction_data)
    
    return {
        'risk_level': risk_level,
        'confidence_score': confidence_score,
        'most_likely_disaster': most_likely_disaster
    }

def process_location(location: str, sector: str) -> Dict[str, Union[str, Dict]]:
    """
    Process location data and return disaster prediction results.
    """
    try:
        weather_data = get_weather_data(location)
        prediction_result = predict_disaster_risk(location, sector, weather_data)
        
        return {
            'District': location,
            'Sector': sector,
            'Temperature': f"{weather_data['temperature']}°C",
            'Wind Speed': f"{weather_data['wind_speed']} m/s",
            'Humidity': f"{weather_data['humidity']}%",
            'Rainfall': f"{weather_data['rainfall']} mm",
            'Soil Type': get_sector_soil_type(rwanda_sectors_dataset_infor, location, sector),
            'Risk Level': prediction_result['risk_level'],
            'Confidence Score': f"{prediction_result['confidence_score']}%",
            'Most Likely Disaster': prediction_result['most_likely_disaster']
        }
    except Exception as e:
        return {'Error': str(e)}






@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_disaster(request):
    location = request.data.get('district')
    sector = request.data.get('sector')

    if not location or not sector:
        return Response({'Error': 'Both district and sector are required'}, status=400)
    
    
    # Check if user has made a prediction in the last 7 days
    one_week_ago = timezone.now() - timedelta(days=7)
    recent_prediction = DisasterPrediction.objects.filter(
        created_by=request.user,
        created_at__gte=one_week_ago
    ).exists()
    
    if recent_prediction:
        print("\n\n You can only make one prediction per week. Please try again later.\n\n")
        return Response({
            'Error': 'You can only make one prediction per week. Please try again later.',
            'next_available': one_week_ago + timedelta(days=7)
        }, status=400)

    result = process_location(location, sector)

    if 'Error' in result:
        return Response(result, status=400)

    # Save prediction result
    prediction = DisasterPrediction.objects.create(
        created_by=request.user,
        district=result.get('District', location),
        sector=result.get('Sector', sector),
        temperature=result.get('Temperature'),
        wind_speed=result.get('Wind Speed'),
        humidity=result.get('Humidity'),
        rainfall=result.get('Rainfall'),
        soil_type=result.get('Soil Type'),
        risk_level=result.get('Risk Level'),
        confidence_score=result.get('Confidence Score'),
        most_likely_disaster=result.get('Most Likely Disaster')
    )

    dps = DisasterPreventionSystem()
    prevention_plan = dps.analyze_prediction(result)
    
    # List to store created prevention strategies
    created_preventions = []

    # Save prevention strategies by timeframe
    for timeframe in ['immediate_actions', 'short_term_actions', 'long_term_actions']:
        if timeframe in prevention_plan['prevention_strategies']:
            for action in prevention_plan['prevention_strategies'][timeframe]:
                prevention_strategy = PreventionStrategy.objects.create(
                    prediction=prediction,
                    action=action['action'],
                    description=action['description'],
                    priority=action['priority'],
                    responsible_entity=action['responsible_entity'],
                    timeframe=timeframe.replace('_', ' ').title(),
                    current_conditions={
                        'temperature': prevention_plan['current_conditions'].get('temperature'),
                        'wind_speed': prevention_plan['current_conditions'].get('wind_speed'),
                        'humidity': prevention_plan['current_conditions'].get('humidity'),
                        'rainfall': prevention_plan['current_conditions'].get('rainfall'),
                        'soil_type': prevention_plan['current_conditions'].get('soil_type')
                    },
                    risk_assessment={
                        'level': prevention_plan['risk_assessment']['level'],
                        'confidence': prevention_plan['risk_assessment']['confidence']
                    },
                    implementation_timeline={
                        'immediate': prevention_plan['timeline'].get('immediate'),
                        'short_term': prevention_plan['timeline'].get('short_term'),
                        'long_term': prevention_plan['timeline'].get('long_term')
                    },
                    resource_requirements={
                        'personnel': prevention_plan['resource_requirements']['personnel'],
                        'equipment': prevention_plan['resource_requirements']['equipment']
                    },
                    budget=prevention_plan['resource_requirements']['estimated_budget'] / len(prevention_plan['prevention_strategies'][timeframe])
                )
                # Add created prevention strategy to the list
                created_preventions.append({
                    'id': prevention_strategy.id,
                    'action': prevention_strategy.action,
                    'description': prevention_strategy.description,
                    'priority': prevention_strategy.priority,
                    'responsible_entity': prevention_strategy.responsible_entity,
                    'timeframe': prevention_strategy.timeframe,
                    'implementation_timeline': prevention_strategy.implementation_timeline,
                    'resource_requirements': prevention_strategy.resource_requirements,
                    'budget': prevention_strategy.budget,
                })

    # Prepare the combined response
    response_data = {
        'prediction': {
            'id': prediction.id,
            'district': prediction.district,
            'sector': prediction.sector,
            'temperature': prediction.temperature,
            'wind_speed': prediction.wind_speed,
            'humidity': prediction.humidity,
            'rainfall': prediction.rainfall,
            'soil_type': prediction.soil_type,
            'risk_level': prediction.risk_level,
            'confidence_score': prediction.confidence_score,
            'most_likely_disaster': prediction.most_likely_disaster,
            'created_at': prediction.created_at,
        },
        'prevention_strategies': created_preventions,
        'analysis_results': result
    }

    return Response(response_data)



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import DisasterPrediction
from .serializers import PredictionSerializer, PreventionStrategySerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_predictions(request):
    try:
        predictions = DisasterPrediction.objects.all()
        serializer = PredictionSerializer(predictions, many=True)
        print(f"\n\n Found Predictions: {serializer.data}\n\n")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_prediction_by_id(request, prediction_id):
    try:
        prediction = DisasterPrediction.objects.get(id=prediction_id)
        serializer = PredictionSerializer(prediction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except DisasterPrediction.DoesNotExist:
        return Response({"error": "Prediction not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_prediction(request, prediction_id):
    try:
        prediction = DisasterPrediction.objects.get(id=prediction_id, created_by=request.user)
        serializer = PredictionSerializer(prediction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except DisasterPrediction.DoesNotExist:
        return Response({"error": "Prediction not found or you do not have permission to update it."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_prediction(request, prediction_id):
    try:
        prediction = DisasterPrediction.objects.get(id=prediction_id, created_by=request.user)
        prediction.delete()
        return Response({"message": "Prediction deleted successfully."}, status=status.HTTP_200_OK)
    except DisasterPrediction.DoesNotExist:
        return Response({"error": "Prediction not found or you do not have permission to delete it."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_predictions(request):
    try:
        # Fetch predictions created by the authenticated user
        predictions = DisasterPrediction.objects.filter(created_by=request.user)
        
        # Serialize predictions
        prediction_serializer = PredictionSerializer(predictions, many=True)
        
        # Fetch all related prevention strategies for the retrieved predictions
        prediction_ids = predictions.values_list('id', flat=True)
        prevention_strategies = PreventionStrategy.objects.filter(prediction_id__in=prediction_ids)
        
        # Serialize prevention strategies
        strategy_serializer = PreventionStrategySerializer(prevention_strategies, many=True)
        
        # Combine both serialized data
        response_data = {
            "predictions": prediction_serializer.data,
            "prevention_strategies": strategy_serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
