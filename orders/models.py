from decimal import Decimal
from django.db import models
from django.urls import reverse 
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator
from core import settings
from essentials.models import Product, Variant, Design
from account.models import Customer, Seller
from coupons.models import Coupon
import json
from django.utils.safestring import mark_safe

from django.contrib.admin.models import LogEntry
from django.core.mail import EmailMultiAlternatives

class Order(models.Model):
    ordered_by = models.ForeignKey(Seller, on_delete=models.CASCADE)
    recipient = models.CharField(max_length=50, blank=True, null=True)
    shipping_label = models.FileField(upload_to='uploads/', blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    note = models.CharField(max_length=1000, blank=True, null=True)
    attachment = models.FileField(upload_to='uploads/', blank=True, null=True, help_text='Check here for gift card')
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                  validators=[MinValueValidator(0),
                                      MaxValueValidator(100)])
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid = models.BooleanField(default=False)
    fulfillment = models.BooleanField(default=False, help_text="Customer will be notified via email if marked.")
    stripe_id = models.CharField(max_length=150, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return f'Order {self.id}'

    def customer_name(self):
        return self.ordered_by.get_customer_name()

    def get_total_cost(self):
        total_cost = sum(item.get_customer_cost() for item in self.items.all())
        return total_cost - total_cost * \
            (self.discount / Decimal(100))

    def cart_total(self):
        total_cost = sum(item.get_customer_cost() for item in self.items.all())
        return total_cost

    def total_item_qty(self):
        total_item = sum(item.quantity for item in self.items.all())
        return total_item

    def get_absolute_url(self):
        return reverse('order_details',
                       args=[self.id])

    def save(self, *args, **kw):
        old = type(self).objects.get(pk=self.pk) if self.pk else None
        super(Order, self).save(*args, **kw)

        if old and old.fulfillment == False and old.fulfillment != self.fulfillment: # if field changed
            print('buna email gonder')
            print(self.ordered_by)
            subject, from_email, to = 'Order #{} Ready!'.format(self.id), settings.DEFAULT_FROM_EMAIL, self.ordered_by
            text_content = 'Order #{} has been processed. See details'.format(self.id)
            html_content = "<p>Order #{} has been processed. See your <a href='https://contextcustom.com/orders/order/'>order history.</a></p>".format(self.id)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()






class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE, null=True, blank=True,
                              )
    variant = models.ForeignKey(Variant,
                                related_name='order_items',
                                on_delete=models.SET_NULL, null=True, blank=True)
    technique = models.CharField(max_length=100, blank=True, null=True)
    placement = models.CharField(max_length=100, blank=True, null=True)
    end_product_img = models.ImageField(upload_to='end_product_imgs/', null=True, blank=True)
    image = models.ImageField(upload_to='designs/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    ready_to_ship = models.BooleanField(default=False)
    log_entry = models.CharField(max_length=200, blank=True, null=True)
    json_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        return str(self.id)

    def customer_name(self):
        return self.order.ordered_by.get_customer_name()

    def recipient(self):
        return self.order.recipient

    def get_customer_cost(self):
        return self.price * self.quantity

    def get_my_cost(self):
        return self.cost * self.quantity

    def dump_json(self):
        return json.dumps(self.json_data)

    def image_tag(self):
        img = self.end_product_img
        if img is not None:
                return mark_safe('<img src="{}" height="150" />'.format(img.url,))

    

    
    