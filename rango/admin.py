from django.contrib import admin
from rango.models import Category, Page, UserProfile
# Register your models here.


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'views', 'likes')
    prepopulated_fields = {"slug":("name",)}


class UserAdmin(admin.ModelAdmin):
    list_display = ("user", )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile, UserAdmin)