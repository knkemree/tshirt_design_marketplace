from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from taggit.managers import TaggableManager
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models import Avg, Count
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from django.contrib.auth.models import Group, Permission, PermissionsMixin
from django.db.models.aggregates import Min


class Category(MPTTModel):
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=False, unique=True)
    description = models.TextField(max_length=255)
    tags = TaggableManager()
    image=models.ImageField(blank=True,upload_to='images/')
    active = models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        unique_together = [['slug', 'title']]

    def get_absolute_url(self):
        return reverse('essentials:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #many to one relation with Category
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=False, unique=True)
    tags = TaggableManager()
    variant_type = models.CharField(max_length=10,choices=VARIANTS, default='None')
    description =RichTextUploadingField(null=True, blank=True)
    image = models.ImageField(upload_to='images/',null=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['slug', 'title']]

    def __str__(self):
        return self.title
    
    def get_lowest_price(self):
        return self.variants.all().aggregate(Min('price'))

    def image_tag(self):
        img = self.image
        if img is not None:
                return mark_safe('<img src="{}" height="150" />'.format(img.url,))



    ## method to create a fake table field in read only mode
    # def cover_image(self):
    #     if self.image.url is not None:
    #         return mark_safe('<img src="{}" height="100"/>'.format(self.image.url))

    # # def get_absolute_url(self):
    # #     return reverse('category_detail', kwargs={'slug': self.slug})
    def get_absolute_url(self):
        return reverse('essentials:product_detail',args=[self.id, self.slug])

    # def avaregereview(self):
    #     reviews = Comment.objects.filter(product=self, status='True').aggregate(avarage=Avg('rate'))
    #     avg=0
    #     if reviews["avarage"] is not None:
    #         avg=float(reviews["avarage"])
    #     return avg

    # def countreview(self):
    #     reviews = Comment.objects.filter(product=self, status='True').aggregate(count=Count('id'))
    #     cnt=0
    #     if reviews["count"] is not None:
    #         cnt = int(reviews["count"])
    #     return cnt

class Size(models.Model):
    name = models.CharField(max_length=20)
    row_no = models.IntegerField(default=0)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['row_no']

class Color(models.Model):
    group = models.CharField(max_length=40, blank=True,null=True, help_text='e.g. black adult tshirts, black youth tshirts, black hoodies (this field only for admins and not visible to customers)')
    name = models.CharField(max_length=40, help_text='e.g black (this field is visible to customers)')
    color_tag = models.ImageField(upload_to='color_tags/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def image_tag(self):
        img = self.color_tag
        if img is not None:
                return mark_safe('<img src="{}" height="50" />'.format(img.url,))

    def product_preview(self):
        images = Mockup.objects.filter(item_color_id=self.id)
        img = images[0]
        if img is not None:
                return mark_safe('<img src="{}" height="100" />'.format(img.image.url,))


class Technique(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name

class Mockup(models.Model):
    item_color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True, related_name='mockups')
    image = models.ImageField(blank=True, upload_to='images/')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('item_color',)

    def __str__(self):
        return 'image-id-'+str(self.id)

    def image_tag(self):
        img = self.image
        if img is not None:
             return mark_safe('<img src="{}" height="150" />'.format(img.url,))

class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    technique = models.ForeignKey(Technique, on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=1)
    cost = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['size','color','technique']

    def __str__(self):
        return self.product.title+str(' / ')+self.size.name+str(' / ')+self.color.name

    def image_tag(self):
        img = self.product.image
        color = self.color.code
        if img is not None:
             return mark_safe('<img src="{}" height="50" style="background-color:{}"/>'.format(img.url, color))
        else:
            return ""

class Design(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT, related_name="designs")
    email = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="designs")
    end_product_img = models.ImageField(upload_to='end_product_imgs/')
    image = models.ImageField(upload_to='designs/')

    def __str__(self):
        return 'Art #'+str(self.id)

    def image_tag(self):
        img = self.product.image
        color = self.color.code
        if img is not None:
             return mark_safe('<img src="{}" height="50" style="background-color:{}"/>'.format(img.url, color))
        else:
            return ""
    

# class ItemType(models.Model):
#     name = models.CharField(max_length=150, help_text="type of Item. ex - accessories, clothing")
#     slug = models.SlugField(max_length=150, unique=True)
#     is_shipping_required = models.BooleanField(default=True)

#     class Meta:
#         ordering = ("slug",)
#         verbose_name = 'Item Type'
#         verbose_name_plural = 'Item Types'
#         app_label = "Item"

#     def __str__(self):
#         return self.name




# class Item(models.Model):
#     item_type = models.ForeignKey(
#         ItemType, related_name="items", on_delete=models.CASCADE
#     )
#     name = models.CharField(max_length=128)
#     slug = models.SlugField()
#     description = models.TextField(blank=True)
#     category = models.ForeignKey(
#         Category,
#         related_name="items",
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#     )
#     article_number = models.CharField(max_length=30)

#     class Meta:
#       verbose_name = "item"
#       verbose_name_plural = "items"
#       ordering = ("name",)
#       constraints = [
#           models.UniqueConstraint(
#               fields=["article_number", "slug"], name="unique article number and slug")
#       ]

#     def __str__(self):
#         return f'{self.name} - {self.article_number}'

# class Attribute(models.Model):
#   name = models.CharField(max_length=200, blank=True)
#   description = models.TextField(blank=True)
#   has_variant = models.BooleanField(default=False)

#   def __str__(self):
#     return self.name


# class AttributeValue(models.Model):
#   attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
#   value = models.CharField(max_length=200, blank=True)
#   description = models.TextField(blank=True)

#   def __str__(self):
#     return self.value


# class ItemAttributeValue(models.Model):
#   item = models.ForeignKey(Item, on_delete=models.CASCADE)
#   attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

#   def __str__(self):
#     return f"{self.item.name} - {self.attribute_value}"


# class ItemTypeAttributeValue(models.Model):
#   item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
#   attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

#   def __str__(self):
#     return f'{self.item_type.name} - {self.attribute_value.value}'


# class ItemVariant(models.Model):
#   sku = models.CharField(max_length=255, unique=True)
#   name = models.CharField(max_length=255, blank=True)
#   item = models.ForeignKey(Item, on_delete=models.CASCADE)
#   price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
#   track_inventory = models.BooleanField(default=True)

#   def __str__(self):
#     return f'{self.item.name} - {self.name}'

# class ItemVariantValues(models.Model):
#   item = models.ForeignKey(Item, on_delete=models.CASCADE)
#   variant = models.ForeignKey(ItemVariant, on_delete=models.CASCADE)
#   value = models.ForeignKey(ItemAttributeValue, on_delete=models.CASCADE)
#   stock = models.PositiveIntegerField(default=0)
#   price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

#   def __str__(self):
#     return f'{self.item.name} - {self.variant.name} - {self.value.attribute_value.value}'


# class ItemImage(models.Model):
#   # just modeling the relationship
#   item = models.ForeignKey(Item, on_delete=models.CASCADE)
#   # image will be here


# class VariantImage(models.Model):
#   # just drawing the relationship
#   variant = models.ForeignKey(ItemVariant, related_name="variant_images", on_delete=models.CASCADE)
#   # Versatilieimagefield.


# class CollectionItem(models.Model):
#     collection = models.ForeignKey(
#         "Collection", related_name="collectionitem", on_delete=models.CASCADE
#     )
#     item = models.ForeignKey(
#         Item, related_name="collectionitem", on_delete=models.CASCADE
#     )

#     class Meta:
#         unique_together = (("collection", "item"),)

#     def get_ordering_queryset(self):
#         return self.item.collectionitem.all()


# class Collection(models.Model):
#     name = models.CharField(max_length=250, unique=True)
#     slug = models.SlugField(max_length=255, unique=True)
#     items = models.ManyToManyField(
#         Item,
#         blank=True,
#         related_name="collections",
#         through=CollectionItem,
#         through_fields=("collection", "item"),
#     )
#     description = models.TextField(blank=True)

#     class Meta:
#         ordering = ("slug",)

#     def __str__(self):
#         return self.name
