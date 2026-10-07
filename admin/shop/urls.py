from django.urls import path

from .views import analytics_dashboard, export_orders_csv, export_sales_csv, export_stock_csv

urlpatterns = [
    path('admin/analytics/', analytics_dashboard, name='analytics_dashboard'),
    path('admin/reports/orders/', export_orders_csv, name='export_orders_csv'),
    path('admin/reports/sales/', export_sales_csv, name='export_sales_csv'),
    path('admin/reports/stock/', export_stock_csv, name='export_stock_csv'),
]
