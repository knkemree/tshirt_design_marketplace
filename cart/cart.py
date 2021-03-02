from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from essentials.models import Design, Product, Variant, Placement, Method
from tasarimlar.models import Design as design_for_sale
from coupons.models import Coupon
import json



class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart  

        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id')    
        

    def add(self, art, variant=None, placement=None, technique=None, end_product_img=None, mockup=None, design=None, json_data=None, quantity=1, override_quantity=False,):
        """
        Add a product to the cart or update its quantity.
        """

        art_id = str(art.uuid)
        # burasi olmazsa update ederken hata veriyor
        try:
            placement = get_object_or_404(Placement, id=placement)
            method = get_object_or_404(Method, id=technique)
        except:
            pass
        if art_id not in self.cart:
            self.cart[art_id] = {'variant':str(variant),
                                    'variant_id':str(variant.id),
                                    'price': str(variant.variant_price()+placement.price+method.method_price()),
                                    'quantity': 0,
                                    'size':str(variant.size),
                                    'color':str(variant.color),
                                    'end_product_img': end_product_img,
                                    'mockup': mockup,
                                    'design': design,
                                    'json_data':json_data,
                                    'technique': str(method),
                                    'placement':str(placement),
                                    'digital_product':False,
                                    'type':'custom',
                                    }
        if override_quantity:
            self.cart[art_id]['quantity'] = quantity
        else:
            self.cart[art_id]['quantity'] += quantity
        self.save()

    def add_design(self, instance_pk, quantity,):
        instance = get_object_or_404(design_for_sale, pk = instance_pk)
        if str(instance.uuid) not in self.cart:
            self.cart[str(instance.uuid)] ={
                                        'title':str(instance.title),
                                        'price':str(instance.price),
                                        'quantity': 1,
                                        'digital_product':True,
                                        'type':'digital'
                                    }
        self.save()

    def add_blank(self, uuid, end_product_img=None, quantity=1, override_quantity=False,):
        variant = get_object_or_404(Variant, uuid=uuid)
        print(override_quantity, 'false omasi lazim')
        if str(variant.uuid) not in self.cart:
            self.cart[str(variant.uuid)] = {
                'title':str(variant),
                'price':str(variant.price),
                'quantity': 0,
                'end_product_img': end_product_img,
                'digital_product':False,
                'type':'blank'
            }

        if override_quantity == True:
            self.cart[str(variant.uuid)]['quantity'] = quantity
        else:
            self.cart[str(variant.uuid)]['quantity'] += quantity
            
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.uuid)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()
        
        products = []
        for i in product_ids:
            try:
                try:
                    p = Design.objects.get(uuid=i)
                    products.append(p)
                except:
                    p = Variant.objects.get(uuid=i)
                    products.append(p)
            except:
                p = design_for_sale.objects.get(uuid=i)
                products.append(p)
        #products = design_for_sale.objects.filter(uuid__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            try:
                cart[str(product.uuid)]['product'] = product
            except:
                #design modelin pk'i uuid olmadigi icin bu exception'i kullanmak gerekiyor. Essentials'daki design modelinin primary key'i uuid olunca bu exception silinebilir
                cart[str(product.uuid)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
        

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None
    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) \
                * self.get_total_price()
        return Decimal(0)
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    # @property
    # def campaign(self):
    #     if self.campaign_id:
    #         try:
    #             return Campaign.objects.get(id=self.campaign_id)
    #         except Campaign.DoesNotExist:
    #             pass
    #     return None
    
    # def get_discount(self):
    #     if self.campaign:
    #         return (self.campaign.campaign_discount / Decimal(100)) \
    #             * self.get_total_price()
    #     return Decimal(0)
    # def get_total_price_after_discount(self):
        
    #     return self.get_total_price() - self.get_discount()

    # @property
    # def shipment(self):
    #     if self.delivery_id:
    #         try:
    #             return Delivery_methods.objects.get(id=self.delivery_id)
    #         except Delivery_methods.DoesNotExist:
    #             pass
    #     return None

    # def shipment_fee(self):
    #     if self.delivery_id:
    #     # delivery'nin kac paradan sonra bedava olacagini burdan ayarliyoruz.
    #         if self.get_total_price_after_discount()>=500:
    #             shipment_fee = Decimal(0)
    
    #             return shipment_fee
    #         else:
    #             shipment_fee = Decimal(self.shipment.fee)
                
    #             return shipment_fee

    # def get_total_price_after_discount_and_shipment_fee(self):
    #     #try except kontrolu koymazsam sag ustteki sepet totalini yapmiyor
    #     try:
    #         return self.get_total_price_after_discount() + self.shipment_fee()
    #     except:
        
    #         return self.get_total_price_after_discount()
    #     #return self.get_total_price_after_discount() + self.shipment.fee()