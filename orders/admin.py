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
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def order_item_detail(obj):
    url = reverse('orders:admin_order_item_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


#@admin_thumbnails.thumbnail('image')
# @admin_thumbnails.thumbnail('image')
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    exclude = ['json_data','cost','end_product_img','image']
    raw_id_fields = ['variant']
    readonly_fields = ('technique','price','quantity','log_entry','placement')
    show_change_link = True
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name','recipient', 
                    'total', 'paid', 'fulfillment',
                    'updated',order_detail,
                    order_pdf,
                    ]
    list_editable = ['fulfillment']
    #search_fields = ['ordered_by',]
    # list_display_links =['customer_name']
    list_filter = ['ordered_by','paid', 'fulfillment','created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
    readonly_fields = ('paid','stripe_id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','order','image_tag','customer_name','recipient','ready_to_ship','log_entry','technique','placement','get_customer_cost','quantity',order_item_detail,'created_at','updated_at']
    list_editable = ['ready_to_ship',]
    readonly_fields = ('log_entry','json_data')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['log_entry','json_data']
        return []