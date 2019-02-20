from django.contrib import admin
from django.contrib import admin
from .models import Product,Stock

class Productadmin(admin.ModelAdmin):
    list_display = ['pid', 'pname', 'pcost','pmfdt','pexpdt']
    list_filter = ['pexpdt','pname']
    class meta:
     model=Product
class Stockadmin(admin.ModelAdmin):
    list_display=['prodid','tot_qty','last_update','next_update']
    list_filter=['prodid']
    class meta:
        model=Stock
admin.site.register(Product,Productadmin)
admin.site.register(Stock,Stockadmin)
