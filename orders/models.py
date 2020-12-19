from django.db import models
from essentials.models import Product, Variant, Design
from account.models import Customer, Seller
from decimal import Decimal
from django.urls import reverse 
from core import settings
#from localflavor.us.forms import USStateSelect

class Order(models.Model):
    ordered_by = models.ForeignKey(Seller, on_delete=models.CASCADE)
    recipient = models.CharField(max_length=50)
    shipping_label = models.FileField(upload_to='uploads/', blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
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

    def get_total_cost(self):
        total_cost = sum(item.get_customer_cost() for item in self.items.all())
        return total_cost

    def cart_total(self):
        total_cost = sum(item.get_customer_cost() for item in self.items.all())
        return total_cost

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
 
    end_product_img = models.ImageField(upload_to='end_product_imgs/', null=True, blank=True)
    image = models.ImageField(upload_to='designs/', null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return str(self.id)

    def get_customer_cost(self):
        return self.price * self.quantity

    def get_my_cost(self):
        return self.cost * self.quantity

    
    