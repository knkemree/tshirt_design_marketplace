from django.contrib import admin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Customer, Comment, Seller
from .forms import UserAdminChangeForm, UserAdminCreationForm


class CustomerAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin','staff','seller','last_login','date_joined')
    list_filter = ('admin','staff','seller')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','phone')}),
        ('Permissions', {'fields': ('user_permissions','groups','admin','staff','seller',
        )}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
        
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','seller')}
        ),
    )
    search_fields = ('email',)
    ordering = ('date_joined',)
    filter_horizontal = ()
    readonly_fields = ('seller','last_login','date_joined')

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment', 'active','create_at']
    list_filter = ['active']
    readonly_fields = ('subject','comment','ip','product','rate','id')

class SellerAdmin(admin.ModelAdmin):
    list_display = ['seller', 'active','email_confirmed']

# class Admin(admin.ModelAdmin):
#     list_display = ['', 'active','email_confirmed']


admin.site.register(Comment, CommentAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Seller, SellerAdmin)
#admin.site.register(, Admin)


    