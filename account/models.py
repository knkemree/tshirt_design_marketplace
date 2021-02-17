from decimal import Decimal
from phonenumber_field.modelfields import PhoneNumberField

from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django.contrib.auth.models import Group, Permission, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from essentials.models import Product
from audioop import reverse



# Create your models here.
class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

            user = self.model(
                email=self.normalize_email(email),
            )

            user.set_password(password)
            user.seller = True
            #user.buyer = True
            user.save(using=self._db)
            return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField("First Name", max_length=30)
    last_name = models.CharField("Last Name", max_length=30)
    phone = PhoneNumberField(null=True, blank=True)
    #user_permissions = models.ManyToManyField(Permission, blank=True)
    #groups = models.ManyToManyField(Group, blank=True)
    admin = models.BooleanField(default=False) # a superuser
    staff = models.BooleanField(default=False) # a admin user; non super-user
    seller = models.BooleanField(default=False, blank=True, null=True)
    stripe_id = models.CharField(max_length=150) 
    is_active = models.BooleanField(default=True)
    remember_me = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    objects = CustomerManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "All Users"


    def get_full_name(self):
        # The user is identified by their email address
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.get_full_name()


    def email_customer(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        
        '''
        from django.core.mail import send_mail
        send_mail(subject, message, from_email, [self.email], **kwargs)

            
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

        # @property
        # def is_active(self):
        #     "Is the user active?"
        #     return self.active

    @property
    def is_seller(self):
        "Is the user seller?"
        return self.seller

class Comment(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    active = models.BooleanField(default=True) 
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']

# class Buyer(models.Model):
#     #name = models.OneToOneField(Customer, on_delete=models.CASCADE,primary_key=True,)
#     buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True, related_name="shopper")
#     active = models.BooleanField(default=False)
#     email_confirmed = models.BooleanField(default=False)
#     timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


#     def __str__(self):
#         return str(self.buyer)

# 	# def get_absolute_url(self):
# 	# 	return reverse("products:vendor_detail", kwargs={"vendor_name": self.user.username})

class Seller(models.Model):
    #email = models.ForeignKey(Customer, on_delete=models.CASCADE,unique=True,)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True, related_name='creator')
    active = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    credit = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.seller)

	# def get_absolute_url(self):
	# 	return reverse("products:vendor_detail", kwargs={"vendor_name": self.user.username})

    # def get_absolute_url(self):
    #     return reverse('seller-detail', kwargs={'pk': self.pk})

    def get_customer_name(self):
        return self.seller.first_name +' '+ self.seller.last_name

    def email(self):
        return self.seller.email

    def user_id(self):
        return self.seller.pk    
     


class Credit(models.Model):
    email = models.ForeignKey(Seller, on_delete=models.PROTECT, blank=True, null=True, related_name='credits')
    STATUS = (
    ('staff', 'Staff'),
    ('seller','Seller'),
    )
    created_by =  models.CharField(max_length=10, choices=STATUS, default='staff')
    added_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    #total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stripe_id = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Credit #{} for {}".format(self.id, self.email.get_customer_name())
