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

class Order(models.Model):
    ordered_by = models.ForeignKey(Seller, on_delete=models.CASCADE)
    recipient = models.CharField(max_length=50, blank=True, null=True)
    shipping_label = models.FileField(upload_to='uploads/', blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    note = models.CharField(max_length=1000, blank=True, null=True)
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
    fulfillment = models.BooleanField(default=False)
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




class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.SET_NULL, null=True, blank=True,
                              )
    variant = models.ForeignKey(Variant,
                                related_name='order_items',
                                on_delete=models.SET_NULL, null=True, blank=True)
    technique = models.CharField(max_length=100, blank=True, null=True)
 
    end_product_img = models.ImageField(upload_to='end_product_imgs/', null=True, blank=True)
    image = models.ImageField(upload_to='designs/', null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    json_data = models.JSONField(blank=True, null=True)


    def __str__(self):
        return str(self.id)

    def get_customer_cost(self):
        return self.price * self.quantity

    def get_my_cost(self):
        return self.cost * self.quantity

    def dump_json(self):
        return json.dumps(self.json_data)

    

    
    