
from django.contrib import admin

from django.contrib.auth.models import Group

import admin_thumbnails
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Product, Color, Size, Technique, Variant, Mockup


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
    #readonly_fields = ('image_tag',)
    extra = 0
    show_change_link = True
    save_as =True
    
@admin_thumbnails.thumbnail('image')
class MockupInline(admin.TabularInline):
    model = Mockup
    extra = 0
    show_change_link = True

@admin_thumbnails.thumbnail('image')
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'active','image_tag']
    list_filter = ['category']
    #readonly_fields = ('image_tag',)
    inlines = [VariantInline]
    prepopulated_fields = {'slug': ('title',)}



class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','group','image_tag']
    list_filter = ['name']
    list_editable = ['group']
    inlines = [MockupInline]

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','row_no']
    list_editable = ['row_no']

class TechniqueAdmin(admin.ModelAdmin):
    list_display = ['name',]

class VariantAdmin(admin.ModelAdmin):
    list_display = ['__str__','technique','color','size','price','quantity','created_at','updated_at']
    list_filter = ['product','size','color','technique']
    #search_fields = ('id','product','size','color','technique',)
    save_as =True

    
@admin_thumbnails.thumbnail('image')
class MockupAdmin(admin.ModelAdmin):
    list_display = ['image_tag','item_color','active']
    list_filter = ['item_color','active']
    

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Technique, TechniqueAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(Mockup, MockupAdmin)
#admin.site.register(Mockup_Group, Mockup_GroupAdmin)
#admin.site.unregister(Group)