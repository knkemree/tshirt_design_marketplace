from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


# Create your models here.
class Expense(models.Model):
    CATEGORY = (
    ('Wage', 'Wage'),
    ('Rent','Rent'),
    ('Utility','Utility'),
    ('Other','Other'),
    )
    category =  models.CharField(max_length=10, choices=CATEGORY, default='Wage')
    title = models.CharField(max_length=100, blank=True, null=True)
    description =RichTextUploadingField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2,default=0, help_text='amount of expense')
    invoice = models.FileField(upload_to='uploads/', blank=True, null=True, help_text='Upload PDF format of the invoice')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
