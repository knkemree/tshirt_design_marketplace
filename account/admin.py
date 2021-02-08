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
    list_display = ('email', 'admin','stripe_id','staff','seller','last_login','date_joined')
    list_filter = ('admin','staff','seller')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','phone')}),
        ('Permissions', {'fields': ('user_permissions','groups','stripe_id','admin','staff','seller',
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
    ordering = ('-date_joined',)
    filter_horizontal = ()
    readonly_fields = ('stripe_id','seller','last_login','date_joined')

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment', 'active','create_at']
    list_filter = ['active']
    readonly_fields = ('subject','comment','ip','product','rate','id')


# class CreditInline(admin.TabularInline):
#     model = Seller
#     #show_change_link = True
#     #extra = 0
#     fields = ['order','amount']
#     #exclude = ['json_data','cost','end_product_img','image']
#     raw_id_fields = ['seller']
#     #readonly_fields = ('item','size','color','preview','technique','placement','price','quantity','ready_to_ship','log_entry','details')
#     #list_editable = ('ready_to_ship',)



class SellerAdmin(admin.ModelAdmin):
    list_display = ['seller', 'active','email_confirmed']
    #inlines = [CreditInline]




admin.site.register(Comment, CommentAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Seller, SellerAdmin)
#admin.site.register(, Admin)


    