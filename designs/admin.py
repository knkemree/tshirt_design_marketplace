from django.contrib import admin
from designs.models import Design, DesignImage, Design_Category
from django.utils.safestring import mark_safe


class Design_CategoryAdmin(admin.ModelAdmin):
    #list_display = '__all__'
    prepopulated_fields = {'slug': ('title',)}

class DesignImageInline(admin.TabularInline):
    model = DesignImage
    extra = 0
    show_change_link = True
    readonly_fields = ['preview']

    def preview(self, obj):
        #return mark_safe("""<img src="/images/%s.jpg" />""" % obj.end_product_img)
        img = obj.image
        if img is not None:
            return mark_safe('<img src="{}" height="150" />'.format(img.url,))

class DesignAdmin(admin.ModelAdmin):
    list_display = ['preview','title','digital_product','price','sales','active']
    list_display_links = ['preview','title']
    list_filter = ['active']
    search_fields = ['title']
    inlines = [DesignImageInline]
    prepopulated_fields = {'slug': ('title',)}

# Register your models here.
admin.site.register(Design, DesignAdmin)
#admin.site.register(DesignImage)
admin.site.register(Design_Category)