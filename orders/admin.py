import admin_thumbnails
import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = 'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not \
    field.many_to_many and not field.one_to_many] 
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'


def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'

def order_detail(obj):
    #return mark_safe(f'<a href="admin/orders/order/{obj.id}/change/">View</a>')
    # url = reverse('orders:admin_order_detail', args=[obj.id])
    # return mark_safe(f'<a href="{url}">View</a>')
    url = reverse('admin:%s_%s_change' % (obj._meta.app_label,  obj._meta.model_name),  args=[obj.id] )
    return mark_safe(f'<a href="{url}">View</a>')
    #return u'<a href="%s">Edit %s</a>' % (url,  obj.__str__)

def order_item_detail(obj):
    url = reverse('orders:admin_order_item_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


#@admin_thumbnails.thumbnail('image')
#@admin_thumbnails.thumbnail('image')
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    show_change_link = True
    extra = 0
    fields = ['preview','item','bundle','is_digital_product','technique','placement','price','quantity','ready_to_ship','log_entry','details']
    #exclude = ['json_data','cost','end_product_img','image']
    raw_id_fields = ['variant','bundle']
    readonly_fields = ('item','size','color','preview','technique','placement','price','quantity','ready_to_ship','log_entry','details','is_digital_product')
    list_editable = ('ready_to_ship',)
    


    def preview(self, obj):
        #return mark_safe("""<img src="/images/%s.jpg" />""" % obj.end_product_img)
        img = obj.end_product_img
        if img is not None:
            return mark_safe('<img src="{}" height="300" />'.format(img.url,))

    def item(self, obj):
        if obj.variant:
            return '{}'.format(obj.variant)
        else:
            return '{}'.format(obj.bundle.title)
            
    def size(self, obj):
        return '{}'.format(obj.variant.size.name)
    def color(self, obj):
        return '{}'.format(obj.variant.color.name)
    def ready_to_ship(self,obj):
        return obj.ready_to_ship
    def details(self, obj):
        id = obj.id
        return mark_safe(f'<a href="/orders/admin/orderitem/{id}/">View</a>')




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name','recipient', 
                    'total', 'paid','status',
                    'updated','created',
                    #order_detail,
                    order_pdf,
                    ]
    #list_editable = ['status']
    search_fields = ['id','ordered_by__seller__first_name','ordered_by__seller__last_name','ordered_by__seller__email','recipient']
    list_display_links =['id',]
    list_filter = ['ordered_by','paid', 'customer_notified','created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
    readonly_fields = ('paid','stripe_id','note')

    

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','order','image_tag','customer_name','recipient','ready_to_ship','log_entry','technique','placement','get_customer_cost','quantity',order_item_detail,'created_at','updated_at']
    list_editable = ['ready_to_ship',]
    actions = [export_to_csv]
    readonly_fields = ('log_entry','json_data')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['log_entry','json_data']
        return []