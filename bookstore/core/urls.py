from django.urls import path
from .views import (
    ItemDetailView,
    search,
    update_username,
    update_email,
    classifications,
    languages,
    categories,
    home,
    contact_us,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    CheckoutView,
    PaymentView,
    purchases_summary,
    AddCouponView,
    RequestRefundView
)

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('update-username/', update_username, name='update-username'),
    path('update-email/', update_email, name='update-email'),
    path('contact-us/', contact_us, name='contact-us'),
    path('classifications/<slug>/', classifications, name='classification'),
    path('languages/<slug>/', languages, name='language'),
    path('categories/<slug>/', categories, name='category'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('purchase-summary/', purchases_summary, name='purchase-summary'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund')
]

