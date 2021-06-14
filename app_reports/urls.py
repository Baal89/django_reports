from django.urls import path
from django.urls import path
from .views import create_reports_view

app_name = 'app_reports'

urlpatterns = [
    path('save/', create_reports_view, name='create-report')
]