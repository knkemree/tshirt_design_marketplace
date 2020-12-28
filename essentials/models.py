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

#from account.models import Customer


#from account.models import Comment





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


    # def __str__(self):                           # __str__ method elaborated later in
    #     full_path = [self.title]                  # post.  use __unicode__ in place of
    #     k = self.parent
    #     while k is not None:
    #         full_path.append(k.title)
    #         k = k.parent
    #     return ' / '.join(full_path[::-1])


class Product(models.Model):
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    #seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
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


# class Image(models.Model):
#     product=models.ForeignKey(Product,on_delete=models.CASCADE)
#     title = models.CharField(max_length=50,blank=True)
#     image = models.ImageField(blank=True, upload_to='images/')

#     def __str__(self):
#         return self.title

class Size(models.Model):
    name = models.CharField(max_length=20)
    #code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=40)
    color_tag = models.ImageField(upload_to='color_tags/', blank=True)

    def __str__(self):
        return self.name

    # def color_tag(self):
    #     if self.code is not None:
    #         return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))

class Mockup(models.Model):
    item_color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True, related_name='mockups')
    #item_color = models.CharField(max_length=50,blank=True)
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


# class Mockup_Group(models.Model):
#     title = models.CharField(max_length=50,blank=True, help_text="name it by color. e.g. 'blue mockups'")
#     group = models.ManyToManyField(Mockup)
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name = 'Mockup Group'
#         verbose_name_plural = 'Mockup Groups'



class Variant(models.Model):
    #title = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    #mockup_group = models.ForeignKey(Mockup_Group, on_delete=models.CASCADE,blank=True,null=True)
    #image_id = models.IntegerField(blank=True,null=True,default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    def __str__(self):
        return self.product.title+str('-')+self.size.name+str('-')+self.color.name

    # def image(self):
    #     img = Image.objects.get(id=self.image_id)
    #     if img.id is not None:
    #          varimage=img.image.url
    #     else:
    #         varimage=""
    #     return varimage

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

    # def image(self):
    #     img = Image.objects.get(id=self.image_id)
    #     if img.id is not None:
    #          varimage=img.image.url
    #     else:
    #         varimage=""
    #     return varimage

    def image_tag(self):
        img = self.product.image
        color = self.color.code
        if img is not None:
             return mark_safe('<img src="{}" height="50" style="background-color:{}"/>'.format(img.url, color))
        else:
            return ""
    


