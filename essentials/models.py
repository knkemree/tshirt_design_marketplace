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
        return str(self.title)

    class MPTTMeta:
        order_insertion_by = ['title']
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        unique_together = [['slug', 'title']]

    def get_absolute_url(self):
        return reverse('essentials:product_list_by_category',
                       args=[self.slug])

class TechniqueBase(models.Model):
    name = models.CharField(max_length=100)
       
    def __str__(self):
        return str(self.name)

class Technique(models.Model):
    technique = models.ForeignKey(TechniqueBase, on_delete=models.CASCADE, blank=True, null=True)
       
    def __str__(self):
        return str(self.technique)


class Product(models.Model):
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #many to one relation with Category
    technique = models.ManyToManyField(Technique, related_name='products', blank=True, null=True)
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
        return str(self.title)
    
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
        return str(self.name)

    class Meta:
        ordering = ['row_no']

class Color(models.Model):
    group = models.CharField(max_length=40, blank=True,null=True, help_text='e.g. black adult tshirts, black youth tshirts, black hoodies (this field only for admins and not visible to customers)')
    name = models.CharField(max_length=40, help_text='e.g black (this field is visible to customers)')
    color_tag = models.ImageField(upload_to='color_tags/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.group)

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
    #technique = models.ForeignKey(Technique, on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=1)
    cost = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['size','color']

    def __str__(self):
        return str(self.product.title+str(' / ')+self.size.name+str(' / ')+self.color.name)

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
