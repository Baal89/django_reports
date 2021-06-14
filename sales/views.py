from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm
from app_reports.forms import ReportForm
import pandas as pd
from .utils import get_salesman_from_id, customer_from_id, get_chart

# Create your views here.

def home_view(request):
    sale_df = None
    position_df = None
    merge_df = None
    df = None
    chart = None
    no_data = None

    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')

        sale_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if len(sale_qs) > 0:
            sale_df = pd.DataFrame(sale_qs.values())
            sale_df['customer_id'] = sale_df['customer_id'].apply(customer_from_id)
            sale_df['salesman_id'] = sale_df['salesman_id'].apply(get_salesman_from_id)
            sale_df['created'] = sale_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sale_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman', 'id': 'sales_id'}, axis=1, inplace=True)
            
            positions_data = []
            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id(),
                    }
                    positions_data.append(obj)

            position_df = pd.DataFrame(positions_data)
            merge_df = pd.merge(sale_df, position_df, on='sales_id')

            df = merge_df.groupby('transaction_id', as_index=False)['price'].agg('sum')

            chart = get_chart(chart_type, sale_df, results_by)

            position_df = position_df.to_html()
            sale_df = sale_df.to_html()
            merge_df = merge_df.to_html()
            df = df.to_html()
        else:
            no_data = 'No data available in this date range'

    context = {
        'search_form': search_form,
        'report_form': report_form,
        'sale_df':sale_df,
        'position_df':position_df,
        'merge_df': merge_df,
        'df': df,
        'chart': chart,
        'no_data': no_data
        }
    return render(request, 'sales/home.html', context)

class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'