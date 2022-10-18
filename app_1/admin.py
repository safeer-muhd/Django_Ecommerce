from django.contrib import admin
from . models import Cart, Catagory,Product
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','image','description')

admin.site.register(Catagory,CategoryAdmin)
admin.site.register(Product)
admin.site.register(Cart)