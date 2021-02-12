from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from taggit.managers import TaggableManager
from django.urls import reverse

# Create your models here.
class Mockup_Category(MPTTModel):
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
        #self.title
        if self.parent:
            return '{} -> {}'.format(self.parent, self.title)
        else:
            return self.title

    class MPTTMeta:
        order_insertion_by = ['title']
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        unique_together = [['slug', 'title']]

    # def get_absolute_url(self):
    #     return reverse('essentials:product_list_by_category',
    #                    args=[self.slug])



class Mockup(models.Model):
    #category = models.ManyToManyField(Mockup_Category, blank=True, null=True)
    BRANDS = (
        ('gildan','Gildan'),
        ('bella-canvas','Bella+Canvas'),
        ('context','Context'),
    )
    brand = models.CharField(max_length=40, choices=BRANDS, blank=True, null=True)
    image=models.ImageField(blank=True,upload_to='images/')
    tags = TaggableManager()
    active = models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return "{} Mockup #{}".format(self.brand, self.id)