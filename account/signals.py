from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.db import transaction

from .models import Customer, Seller

@receiver(post_save, sender=Customer)
def create_seller_profile(sender, instance, created, **kwargs):
    if created and instance.seller == True:
        new_seller  = Seller.objects.create(seller=instance)
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