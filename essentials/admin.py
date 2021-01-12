
from django.contrib import admin

from django.contrib.auth.models import Group

import admin_thumbnails
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Product, Color, Size, Technique, TechniqueBase, Variant, Mockup, Design

#Method, Placement, PlacementBase



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
    #fields = ['render_image',]
    #readonly_fields = ('image_tag',)
    extra = 0
    show_change_link = True
    save_as =True
    ordering = ["color","size",]

    # def render_image(self, obj):
    #     images = Mockup.objects.filter(item_color_id=obj.color.id)
    #     img = images[0]
    #     if img is not None:
    #         return mark_safe("""<img src="/images/%s.jpg" />""" % obj.image)
    
@admin_thumbnails.thumbnail('image')
class MockupInline(admin.TabularInline):
    model = Mockup
    extra = 0
    show_change_link = True

# class MethodInline(admin.TabularInline):
#     model = Method
#     extra = 0
#     show_change_link = True

# class PlacementInline(admin.TabularInline):
#     model = Placement
#     extra = 0
#     show_change_link = True

@admin_thumbnails.thumbnail('image')
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'active','image_tag']
    list_filter = ['category']
    #readonly_fields = ('image_tag',)
    inlines = [VariantInline, 
    #MethodInline, PlacementInline
    ]
    prepopulated_fields = {'slug': ('title',)}



class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','group','image_tag','created_at','updated_at',]
    list_filter = ['name','created_at','updated_at',]
    list_editable = ['group',]
    search_fields = ['name',]
    inlines = [MockupInline]

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','row_no',]
    list_editable = ['row_no',]
    search_fields = ['name',]

class TechniqueAdmin(admin.ModelAdmin):
    list_display = ['technique',]
    search_fields = ['technique',]

class VariantAdmin(admin.ModelAdmin):
    list_display = ['__str__','size','color','price','quantity','created_at','updated_at',]
    list_filter = ['product','size','color',]
    search_fields = ['size','color',]
    save_as =True

    
@admin_thumbnails.thumbnail('image')
class MockupAdmin(admin.ModelAdmin):
    list_display = ['image_tag','item_color','active']
    list_filter = ['item_color','active']


# need to work on inline admin 
# class ItemAdmin(admin.TabularInline):
#   model = Item
#   extra = 2

# class ItemTypeAdmin(admin.ModelAdmin):
#   inlines = [ItemAdmin]

# admin.site.register(models.Product, ProductAdmin)
# admin.site.register(models.ProductType, ProductTypeAdmin)
# admin.site.register(Item)
# admin.site.register(ItemType)
# admin.site.register(Attribute)
# admin.site.register(AttributeValue)
# admin.site.register(ItemAttributeValue)
# admin.site.register(ItemTypeAttributeValue)
# admin.site.register(ItemVariant)
# admin.site.register(ItemVariantValues)
# admin.site.register(Collection)
    
admin.site.register(Design)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(TechniqueBase)
admin.site.register(Technique, TechniqueAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(Mockup, MockupAdmin)
# admin.site.register(Method)
# admin.site.register(Placement)
# admin.site.register(PlacementBase)
#admin.site.register(Mockup_Group, Mockup_GroupAdmin)
#admin.site.unregister(Group)