from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('api/services-by-location/', views.get_services_by_location, name='services_by_location'),
    path('api/employees-by-location/', views.get_employees_by_location, name='employees_by_location'),
]
