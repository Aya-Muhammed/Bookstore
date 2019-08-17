from django import template
from core.models import Order

register = template.Library()


@register.filter
def order_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=True)
        if qs.exists():
            return qs[0].items.count()
    return 0
