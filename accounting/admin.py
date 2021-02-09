from django.contrib import admin
from accounting.models import Expense

# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['title','category','amount','invoice','created_at','updated_at']
    list_filter = ['category','created_at','updated_at']
    list_editable = [
        'amount',
        'category']
    #readonly_fields = ('image_tag',)

admin.site.register(Expense, ExpenseAdmin)