import os
import uuid
from mptt.models import MPTTModel
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import TreeForeignKey
from taggit.managers import TaggableManager

from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe



# Create your models here.
class Design_Category(MPTTModel):
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=False, unique=True)
    description = models.TextField(max_length=255)
    #tags = TaggableManager()
    image=models.ImageField(blank=True,upload_to='images/')
    active = models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        unique_together = [['slug', 'title']]

    def __str__(self):
        #self.title
        if self.parent:
            return '{} -> {}'.format(self.parent, self.title)
        else:
            return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    

    # def get_absolute_url(self):
    #     return reverse('essentials:product_list_by_category',
    #                    args=[self.slug])





class DesignActivatedManager(models.Manager):
    def get_queryset(self):
        return super(DesignActivatedManager, self).get_queryset().filter(active=True)


class Design(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    departments = models.ManyToManyField(Design_Category, blank=False, null=True, related_name='designs')
    title = models.CharField(max_length=40, blank=False, null=True, unique=True,)
    slug = models.SlugField(blank=False, null=False, unique=True)
    digital_product = models.FileField(blank=False, null=True, upload_to='digital_products/', help_text="Customer will download this file upon succesfull payment")
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=True, help_text="price for this digital product")
    cost = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=True, help_text="cost for this digital product")
    sales = models.IntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    description =RichTextUploadingField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    # Model managers
    objects = models.Manager()  # The default manager.
    activated = DesignActivatedManager()  # Our custom manager.

    class Meta:
        unique_together = [['slug', 'title']]
        ordering = ['created_at','updated_at']

    def __str__(self):
        return "{}".format(self.title)

    def preview(self):
        img = self.design_images.first()
        if img is not None:
                return mark_safe('<img src="{}" height="150" />'.format(img.image.url,))

    def get_absolute_url(self):
        return reverse('designs:design-detail',args=[self.slug])


class DesignImageActivatedManager(models.Manager):
    def get_queryset(self):
        return super(DesignImageActivatedManager, self).get_queryset().filter(active=True)

class DesignImage(models.Model):
    #design = models.ForeignKey(Design, on_delete=models.SET_NULL, null=True, blank=True, related_name='design_images', to_field='uuid')
    tasarim = models.ForeignKey(Design, on_delete=models.SET_NULL, null=True, blank=False, related_name='design_images', to_field='uuid')
    image = models.ImageField(upload_to='designs/%Y/%m/%d', blank=False, null=True)
    row_no = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Model managers
    objects = models.Manager()  # The default manager.
    activated = DesignImageActivatedManager()  # Our custom manager.

    class Meta:
        ordering = ['row_no']

    def __str__(self): 
        return os.path.basename(self.image.name)
        #return self.product.name

    

    