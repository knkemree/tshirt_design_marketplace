from django.db.models.signals import post_save, pre_delete, post_delete, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Variant, Product, Size, Color,Sz, Clr
from django.shortcuts import get_object_or_404


@receiver(post_save, sender=Clr)
def creat_color(sender, instance, **kwargs):

    #eger birden fazla bu renkten varsa ilki haric hepsini sil.
    is_duplicated = Clr.objects.filter(product=instance.product, clr=instance.clr)
    if len(is_duplicated) > 1:
        for i in is_duplicated[1:]:    
            i.delete()

    for size in instance.product.szs.all():
        
        #get_or_create kullanilamaz cunku size ve colora gore al yokda price'i da ekle. fiyatlar farkli olursa double yaoiyor fiyatlari farkli oluyor
        try:
            vr = Variant.objects.get(product=instance.product, color=instance.clr, size=size.sz)
            vr.price = size.price+instance.price
            vr.save()
        except:
            Variant.objects.create(product=instance.product, color=instance.clr, size=size.sz, price = size.price+instance.price)
            
        
        print(instance.id, 'clr instance')
        print(instance.product.clrs.all())

@receiver(post_save, sender=Sz)
def creat_size(sender, instance, created, **kwargs):

    #eger birden fazla bu sizedan varsa ilki haric hepsini sil.
    is_duplicated = Sz.objects.filter(product=instance.product, sz=instance.sz)
    if len(is_duplicated) > 1:
        for i in is_duplicated[1:]:    
            i.delete()

    for color in instance.product.clrs.all():

        #get_or_create kullanilamaz cunku size ve colora gore al yokda price'i da ekle. fiyatlar farkli olursa double yaoiyor fiyatlari farkli oluyor
        try:
            vr = Variant.objects.get(product=instance.product, size=instance.sz, color=color.clr)
            vr.price = color.price+instance.price
            vr.save()
        except:
            Variant.objects.create(product=instance.product, size=instance.sz, color=color.clr, price = color.price+instance.price)
        
        print(instance.id, 'sz instance')
        print(instance.product.clrs.all())
        print(instance.product.szs.all())

@receiver(post_delete, sender=Clr)
def delete_color(sender, instance, **kwargs):
    
    vrs = Variant.objects.filter(product=instance.product, color=instance.clr)
    for i in vrs:
        i.delete()
        

@receiver(post_delete, sender=Sz)
def delete_size(sender, instance, **kwargs):
    
    vrs = Variant.objects.filter(product=instance.product, size=instance.sz)
    for i in vrs:
        i.delete()
    
        