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
        'user', 'get_html_photo', 'photo_name', 'create_at', 'updated_at',
        'moderation')
    list_filter = ('moderation',)
    readonly_fields = ('create_at', 'updated_at',)
    list_editable = ('moderation',)
    prepopulated_fields = {'slug': ('photo_name',)}

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = 'фото'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content',)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('photo', 'user')


admin.site.register(models.Usermodels.User, UserAdmin)
admin.site.register(models.Photomodels.Photo, PhotoAdmin)
admin.site.register(models.Commentmodels.Comment, CommentAdmin)
admin.site.register(models.Likemodels.Like, LikeAdmin)
# Register your models here.
