from datetime import date
from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'get_html_photo', 'email')
    list_filter = ('first_name', 'last_name', 'is_superuser')
    ordering = ('username',)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = 'фото'


class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'get_html_photo', 'photo_name', 'create_at', 'updated_at',
        'moderation')
    list_filter = ('moderation', 'user')
    list_editable = ('moderation',)
    ordering = ('create_at', 'photo_name', 'user')
    readonly_fields = ('create_at', 'updated_at',)
    search_fields = ('photo_name',)
    prepopulated_fields = {'slug': ('photo_name',)}

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = 'фото'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('photo', 'get_html_photo', 'user', 'content', 'create_at', 'updated_at',)
    list_filter = ('photo',)
    ordering = ('create_at', 'user',)
    search_fields = ('user__username', 'content')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.photo.url}' width=50>")

    get_html_photo.short_description = 'фото'


class LikeAdmin(admin.ModelAdmin):
    list_display = ('get_html_photo', 'user')
    list_editable = ('user',)
    list_filter = ('user',)
    ordering = ('user',)
    search_fields = ('user__username',)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.photo.url}' width=50>")

    get_html_photo.short_description = 'фото'


admin.site.register(models.Usermodels.User, UserAdmin)
admin.site.register(models.Photomodels.Photo, PhotoAdmin)
admin.site.register(models.Commentmodels.Comment, CommentAdmin)
admin.site.register(models.Likemodels.Like, LikeAdmin)
# Register your models here.
