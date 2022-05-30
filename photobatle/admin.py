import datetime

from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models


class UserAdmin(admin.ModelAdmin):
    '''Переопределенная модель user в админке'''
    list_display = ('username', 'first_name', 'last_name', 'get_html_photo', 'email')
    list_filter = ('first_name', 'last_name', 'is_superuser')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = 'фото'


class PhotoAdmin(admin.ModelAdmin):
    '''Модель фото в админке'''
    prepopulated_fields = {'slug':('photo_name',)}
    list_display = (
        'user_name', 'get_html_photo', 'photo_name', 'date_published_on_site', 'like_count',
        'comment_count', 'moderation')
    list_filter = ('moderation',)
    readonly_fields = ('date_published_on_site','like_count', 'comment_count',)
    list_editable = ('moderation',)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = 'фото'


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Photo, PhotoAdmin)
# Register your models here.
