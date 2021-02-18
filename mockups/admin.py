import admin_thumbnails
from django.contrib import admin
from mockups.models import Mockup, Mockup_Category
# Register your models here.

@admin_thumbnails.thumbnail('image')
class MockupAdmin(admin.ModelAdmin):
    list_display = ['id','preview','title', 'brand','active','created_at']
    prepopulated_fields = {'slug': ('title',)}
    list_display_links = ['id','preview']
    list_filter = ['active','created_at','brand']
    search_fields = ['title','brand','id']
    #readonly_fields = ('subject','comment','ip','product','rate','id')

admin.site.register(Mockup, MockupAdmin)
admin.site.register(Mockup_Category)