from django.shortcuts import render, get_object_or_404
from profiles.models import Profile
from django.http import JsonResponse
from .utils import get_report_image
from .models import Report
from django.views.generic import ListView, DetailView, TemplateView

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from sales.models import Sale, Position, CSV
import csv
# Create your views here.

class ReportListView(ListView):
    model = Report
    template_name = 'app_reports/main.html'

class ReportDetailView(DetailView):
    model = Report
    template_name = 'app_reports/detail.html'

class UploadTemplateView(TemplateView):
    template_name = 'app_reports/from_file.html'

def csv_upload_view(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file')
        obj = CSV.objects.create(file_name=csv_file)

        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)
            reader.__next__()
            for row in reader:
                print(row, type(row))

    return HttpResponse

def create_reports_view(request):
    if request.is_ajax():
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')

        img = get_report_image(image)

        author = Profile.objects.get(user=request.user)
        Report.objects.create(name=name, remarks=remarks, image=img, author=author)
        return JsonResponse({'msg': 'send'})
    return JsonResponse({})

def render_pdf_view(request, pk):
    obj = get_object_or_404(Report, pk=pk)
    template_path = 'app_reports/pdf.html'
    context = {'obj': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # if download 
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if display 
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response