import csv
from django.shortcuts import render
from django.http import HttpResponse
from Services.models import Order, Address

def generate_end_of_month_report(request):
    """
    Generate a CSV report containing order and customer details.
    """
    if request.method == "POST":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="end_of_month_report.csv"'

      
        writer = csv.writer(response)
        writer.writerow([
            'Order ID', 'Customer Name', 'Email', 'Phone', 'Location',
            'Order Date', 'Grand Total', 'Payment Status'
        ])

        # Query data (e.g., all orders for the current month, limited to 100 rows)
        orders = Order.objects.select_related('customer').all()[:100]

        for order in orders:
            location = order.customer.address.location if order.customer and order.customer.address else "N/A"
            writer.writerow([
                order.orderID,
                order.customer.name if order.customer else "N/A",
                order.customer.email if order.customer else "N/A",
                order.customer.phone if order.customer and order.customer.phone else "N/A",
                location,
                order.order_date.strftime("%Y-%m-%d"),
                order.grand_total,
                order.get_payment_status_display() if order.payment_status else "N/A",
            ])

        return response  # Return the CSV response here

    return render(request, 'generate_report.html')
