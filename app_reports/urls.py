from django.urls import path
from django.urls import path
from .views import (
    create_reports_view,
    ReportDetailView,
    ReportListView,
    UploadTemplateView,
    render_pdf_view,
    csv_upload_view,
)

app_name = 'app_reports'

urlpatterns = [
    path('', ReportListView.as_view(), name='main'),
    path('save/', create_reports_view, name='create-report'),
    path('from_file/', UploadTemplateView.as_view(), name='from-file'),
    path('upload/', csv_upload_view, name='upload'),
    path('<pk>/pdf/', render_pdf_view, name='pdf'),
    path('<pk>/', ReportDetailView.as_view(), name='detail'),
]