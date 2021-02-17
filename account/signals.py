from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.db import transaction

from .models import Customer, Seller
from django.shortcuts import get_object_or_404

@receiver(post_save, sender=Customer)
def create_seller_profile(sender, instance, created, **kwargs):
    if created and instance.seller == True:
        print(instance, 'customer object?')
        customer_instance = get_object_or_404(Customer, email=instance.email)
        new_seller  = Seller.objects.create(seller=customer_instance) # seller mutlaka customer instance olmasi gerkiyor. 
        new_seller.save()
        
        # new_buyer = Buyer.objects.create(buyer=instance)
        # new_buyer.save()

    # if created and instance.seller == False:
    #     new_buyer = Buyer.objects.create(buyer=instance)
    #     new_buyer.save()


@receiver(post_delete, sender=Seller)
#@transaction.atomic
def delete_customer_profile(sender, instance, **kwargs):
    try:
        customer_account = Customer.objects.get(email=instance)
        customer_account.delete()  
    except:
        pass

# @receiver(post_delete, sender=Buyer)
# #@transaction.atomic
# def delete_customer_profile(sender, instance, **kwargs):
#     try:
#         customer_account = Customer.objects.get(email=instance)
#         customer_account.delete()  
#     except:
#         pass