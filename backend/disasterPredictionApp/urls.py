
from django.urls import path
from .views import (
    predict_disaster,
    get_all_predictions,
    get_prediction_by_id,
    get_user_predictions,
    update_prediction,
    delete_prediction
)

urlpatterns = [
    path('predict/', predict_disaster, name='predict'),
    path('predictions/', get_all_predictions, name='get_all_predictions'),
    path('<int:prediction_id>/', get_prediction_by_id, name='get_prediction_by_id'),
    path('user/', get_user_predictions, name='get_user_predictions'),
    path('update/<int:prediction_id>/', update_prediction, name='update_prediction'),
    path('delete/<int:prediction_id>/', delete_prediction, name='delete_prediction'),
]
