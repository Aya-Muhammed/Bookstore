from datetime import date
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.datetime_safe import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)


class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class PublishHouse(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Classification(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:classification', kwargs={
            'slug': self.slug
        })


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:language', kwargs={
             'slug': self.slug
        })


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('core:category', kwargs={
             'slug': self.slug
        })


class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    subject = models.CharField(max_length=20)
    message = models.TextField(max_length=400)

    def __str__(self):
        return f'Message from {self.name}'


class Item(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(default='test-text', blank=False, null=False)
    overview = models.TextField(blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False)
    price = models.FloatField(default=0)
    date_added = models.DateField(default=date.today)
    image = models.ImageField(upload_to='items/', default='items/book.jpg', blank=False, null=False)
    discount_price = models.FloatField(blank=True, null=True)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, blank=False, null=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=False, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=False, null=False)
    publish_house = models.ForeignKey(PublishHouse, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_shipping_fees(self):
        shipping_fees = 0
        if self.item.price == 5.0 or self.item.price <= 10.0:
            return shipping_fees
        return shipping_fees == self.quantity * 10

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price() + self.get_shipping_fees()
        return self.get_total_item_price() + self.get_shipping_fees()


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(default=datetime.now)
    ordered_date = models.DateTimeField(default=datetime.now)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    ready_for_shipping = models.BooleanField(default=True)
    out_for_delivery = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    phone = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.pk}"








