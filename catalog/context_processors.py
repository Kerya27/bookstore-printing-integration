from .models import Order

def admin_stats(request):
    if request.user.is_authenticated and request.user.is_staff:
        return {'orders_new_count': Order.objects.filter(status='new').count()}
    return {}