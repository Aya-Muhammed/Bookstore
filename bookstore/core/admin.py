from django.contrib import admin

from .models import Item, OrderItem, Order, Author, PublishHouse, Classification, Payment, Coupon, Refund, Address, UserProfile, Contact, Language, Category


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


def make_ready_for_shipping(modeladmin, request, queryset):
    queryset.update(ready_for_shipping=True)


make_ready_for_shipping.short_description = 'Update orders to ready for shipping'


def make_out_for_delivery(modeladmin, request, queryset):
    queryset.update(out_for_delivery=True, ready_for_shipping=False)


make_out_for_delivery.short_description = 'Update orders to out for delivery'


def make_being_delivered(modeladmin, request, queryset):
    queryset.update(being_delivered=True, out_for_delivery=False)


make_being_delivered.short_description = 'Update orders to being delivered'


def make_received(modeladmin, request, queryset):
    queryset.update(received=True, being_delivered=False)


make_received.short_description = 'Update orders to being received'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'ready_for_shipping',
                    'out_for_delivery',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'payment',
                    'coupon',
                    'address'
                    ]
    list_display_links = [
        'user',
        'payment',
        'coupon',
        'address']
    list_filter = ['ordered',
                   'ready_for_shipping',
                   'out_for_delivery',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = ['user__username',
                     'ref_code']
    actions = [make_refund_accepted, make_ready_for_shipping, make_out_for_delivery, make_being_delivered, make_received]


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'city',
                    'area',
                    'street_name',
                    'mobile',
                    'default'
                    ]

    list_filter = ['default', 'city']
    search_fields = ['user', 'city']


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Author)
admin.site.register(PublishHouse)
admin.site.register(Classification)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
admin.site.register(Contact)
admin.site.register(Language)
admin.site.register(Category)



