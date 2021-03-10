
import admin_thumbnails
from mptt.admin import DraggableMPTTAdmin
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from .models import Category, Product, Color, Size, TechniqueBase, Variant, Design, Method, Placement, PlacementBase, Font, Clr, Sz



# Register your models here.

@admin_thumbnails.thumbnail('image')
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class VariantInline(admin.TabularInline):
    model = Variant
    extra = 0
    show_change_link = True
    save_as =True
    ordering = ["color","size",]
    fields = ['color_tag','color','size','quantity','cost','price','sale_price','is_published']
    readonly_fields = ['color_tag','cost','price','color','size']

    def has_delete_permission(self, request, obj=None):
        return False

    def color_tag(self, obj):
        #return mark_safe("""<img src="/images/%s.jpg" />""" % obj.end_product_img)
        if obj.color.texture:
            return mark_safe('<div style="background-image:url({}); height:50px; width:50px;"></div>'.format(obj.color.texture.url,))
        else:
            color = obj.color.color_code
            if color is not None:
                return mark_safe('<div style="background-color:{}; height:50px; width:50px;"></div>'.format(color,))

class SzInline(admin.TabularInline):
    model = Sz
    extra = 1
    show_change_link = True

class ClrInline(admin.TabularInline):
    model = Clr
    extra = 1
    show_change_link = True
    fields = ['color_tag','clr','price','row_no']
    readonly_fields = ['color_tag',]

    def color_tag(self, obj):
        #return mark_safe("""<img src="/images/%s.jpg" />""" % obj.end_product_img)
        if obj.clr.texture:
            return mark_safe('<div style="background-image:url({}); height:50px; width:50px;"></div>'.format(obj.clr.texture.url,))
        else:
            color = obj.clr.color_code
            if color is not None:
                return mark_safe('<div style="background-color:{}; height:50px; width:50px;"></div>'.format(color,))

class MethodInline(admin.TabularInline):
    model = Method
    extra = 0
    show_change_link = True

class PlacementInline(admin.TabularInline):
    model = Placement
    extra = 0
    show_change_link = True
    fields = ['preview','placement','row_no','price','image','width','height','top','left']
    readonly_fields = ('preview',)

    def preview(self, obj):
        #return mark_safe("""<img src="/images/%s.jpg" />""" % obj.end_product_img)
        img = obj.image
        if img is not None:
            return mark_safe('<img src="{}" height="150" />'.format(img.url,))

@admin_thumbnails.thumbnail('image')
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','image_tag','title',
    'brand',
    'variant_type','active','created_at','updated_at']
    list_display_links = ['id','image_tag','title']
    list_filter = ['category','active','created_at','updated_at','brand']
    list_editable = [
        'brand',
        'active']
    search_fields = ['title','brand','id']
    filter_horizontal = ('category',)
    #readonly_fields = ('image_tag',)
    inlines = [ 
    MethodInline, 
    PlacementInline,
    SzInline,
    ClrInline,
    VariantInline,
    ]
    prepopulated_fields = {'slug': ('title',)}



class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','group','created_at','updated_at',]
    list_filter = ['name','created_at','updated_at',]
    list_editable = ['group',]
    search_fields = ['name',]

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','row_no',]
    list_editable = ['row_no',]
    search_fields = ['name',]

class VariantAdmin(admin.ModelAdmin):
    list_display = ['id','__str__','size','color','price','quantity','created_at','updated_at',]
    list_filter = ['product','size','color',]
    search_fields = ['size','color',]
    save_as =True

class DesignAdmin(admin.ModelAdmin):
    list_display = ['id','image_tag','email','variant',]
    list_display_links = ['id','image_tag']
    
admin.site.register(Design, DesignAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
# admin.site.register(Variant, VariantAdmin)
#admin.site.register(Method)
#admin.site.register(Placement)
# admin.site.register(Sz)
# admin.site.register(Clr)
#admin.site.register(ClrBase)
#admin.site.register(SzBase)
admin.site.register(TechniqueBase)
admin.site.register(PlacementBase)
admin.site.register(Font)