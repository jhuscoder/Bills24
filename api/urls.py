from django.urls import path
from .views import API


urlpatterns = [    
    path("", API.as_view(), name="api-health"),
]