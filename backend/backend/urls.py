
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userApp.urls')),
    path('prediction/', include('disasterPredictionApp.urls')),
    path('prevention/', include('disasterPreventionApp.urls')),
]
