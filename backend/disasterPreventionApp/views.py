from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import PreventionStrategy
from .serializers import PreventionStrategySerializer
from disasterPredictionApp.models import DisasterPrediction


# Get all Prevention Strategies
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_preventions(request):
    try:
        preventions = PreventionStrategy.objects.all()
        serializer = PreventionStrategySerializer(preventions, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"Error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Get Prevention Strategy by ID
@api_view(['GET'])
@permission_classes([AllowAny])
def get_prevention_by_id(request, id):
    try:
        prevention = PreventionStrategy.objects.get(id=id)
        serializer = PreventionStrategySerializer(prevention)
        return Response(serializer.data)
    except PreventionStrategy.DoesNotExist:
        return Response({"Error": "Prevention strategy not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"Error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Get Preventions associated with predictions created by the logged-in user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_preventions(request):
    try:
        # Get predictions created by the logged-in user
        predictions = DisasterPrediction.objects.filter(created_by=request.user)

        # Get all strategies related to these predictions
        preventions = PreventionStrategy.objects.filter(prediction__in=predictions)
        serializer = PreventionStrategySerializer(preventions, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"Error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Update Prevention Strategy
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_prevention(request, id):
    try:
        prevention = PreventionStrategy.objects.get(id=id)

        # Check if the logged-in user is the one who created the associated disaster prediction
        if prevention.prediction.created_by != request.user:
            return Response({"Error": "You are not authorized to update this prevention strategy."}, status=status.HTTP_403_FORBIDDEN)

        # Deserialize and validate the input data
        serializer = PreventionStrategySerializer(prevention, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except PreventionStrategy.DoesNotExist:
        return Response({"Error": "Prevention strategy not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"Error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Delete Prevention Strategy
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_prevention(request, id):
    try:
        prevention = PreventionStrategy.objects.get(id=id)

        # Check if the logged-in user is the one who created the associated disaster prediction
        # if prevention.prediction.created_by != request.user:
        #     return Response({"Error": "You are not authorized to delete this prevention strategy."}, status=status.HTTP_403_FORBIDDEN)

        # Delete the prevention strategy
        prevention.delete()
        return Response({"Message": "Prevention strategy deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    except PreventionStrategy.DoesNotExist:
        return Response({"Error": "Prevention strategy not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"Error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
