from django.urls import path
from . import views

urlpatterns = [
    # Get all preventions
    path('preventions/', views.get_all_preventions, name='get_all_preventions'),
    
    # Get prevention by ID
    path('preventions/<int:id>/', views.get_prevention_by_id, name='get_prevention_by_id'),
    
    # Get preventions for the logged-in user
    path('user/', views.get_user_preventions, name='get_user_preventions'),
    
    # Update prevention by ID
    path('update/<int:id>/', views.update_prevention, name='update_prevention'),
    
    # Delete prevention by ID
    path('delete/<int:id>/', views.delete_prevention, name='delete_prevention'),
    path('<int:id>/status/', views.update_prevention_status, name='update_prevention_status'),
]
