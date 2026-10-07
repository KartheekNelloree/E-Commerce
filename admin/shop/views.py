import csv

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Sum
from django.http import HttpResponse

from .models import Order, Payment, Product


@staff_member_required
def analytics_dashboard(request):
    total_sales = Order.objects.filter(payment_status='PAID').aggregate(total=Sum('total_amount'))['total'] or 0
    total_orders = Order.objects.count()
    successful_payments = Payment.objects.filter(status='PAID').count()
    failed_payments = Payment.objects.filter(status='FAILED').count()
    average_order_value = Order.objects.filter(payment_status='PAID').aggregate(avg=Avg('total_amount'))['avg'] or 0
    top_products = Product.objects.filter(is_active=True).order_by('-popularity_score')[:5]
    low_stock_products = Product.objects.filter(stock__lt=10).order_by('stock')[:5]
    recent_orders = Order.objects.order_by('-created_at')[:5]

    rows = [
        ['Metric', 'Value'],
        ['Total sales', f'USD {total_sales}'],
        ['Total orders', total_orders],
        ['Successful payments', successful_payments],
        ['Failed payments', failed_payments],
        ['Average order value', f'USD {average_order_value}'],
    ]

    content = '<html><body><h1>Admin Analytics</h1><table>'
    for key, value in rows:
        content += f'<tr><td>{key}</td><td>{value}</td></tr>'
    content += '</table>'
    content += '<h2>Top products</h2><ul>'
    for product in top_products:
        content += f'<li>{product.name} ({product.popularity_score})</li>'
    content += '</ul>'
    content += '<h2>Low stock</h2><ul>'
    for product in low_stock_products:
        content += f'<li>{product.name} ({product.stock} left)</li>'
    content += '</ul>'
    content += '<h2>Recent orders</h2><ul>'
    for order in recent_orders:
        content += f'<li>#{order.id} - {order.total_amount} - {order.order_status}</li>'
    content += '</ul></body></html>'
    return HttpResponse(content)


@staff_member_required
def export_orders_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'user', 'total_amount', 'order_status', 'payment_status', 'created_at'])
    for order in Order.objects.all().order_by('-created_at'):
        writer.writerow([order.id, order.user.email, order.total_amount, order.order_status, order.payment_status, order.created_at])
    return response


@staff_member_required
def export_sales_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales.csv"'
    writer = csv.writer(response)
    writer.writerow(['order_id', 'user', 'total_amount', 'payment_status'])
    for order in Order.objects.filter(payment_status='PAID').order_by('-created_at'):
        writer.writerow([order.id, order.user.email, order.total_amount, order.payment_status])
    return response


@staff_member_required
def export_stock_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stock.csv"'
    writer = csv.writer(response)
    writer.writerow(['product', 'category', 'stock', 'price'])
    for product in Product.objects.all().order_by('stock'):
        writer.writerow([product.name, product.category, product.stock, product.price])
    return response
