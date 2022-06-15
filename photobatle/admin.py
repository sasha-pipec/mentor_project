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
    list_display = (
        'user_name', 'get_html_photo', 'photo_name', 'date_published_on_site', 'like_count',
        'moderation')
    list_filter = ('moderation',)
    readonly_fields = ('date_published_on_site', 'like_count')
    list_editable = ('moderation',)
    prepopulated_fields = {'slug': ('photo_name',)}

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = 'фото'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content',)


admin.site.register(models.Usermodels.User, UserAdmin)
admin.site.register(models.Photomodels.Photo, PhotoAdmin)
admin.site.register(models.Commentmodels.Comment, CommentAdmin)
# Register your models here.
