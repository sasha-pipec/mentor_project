from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialToken, SocialApp, SocialAccount

from rest_framework.authtoken.models import TokenProxy
from rest_framework.exceptions import ValidationError

from photobatle.service import *
from photobatle.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'get_html_photo', 'email')
    list_filter = ('first_name', 'last_name', 'is_superuser')
    ordering = ('username',)
    exclude = ('password', 'groups', 'user_permissions')

    def get_readonly_fields(self, request, obj):
        if obj:
            return self.readonly_fields + (
            'last_login', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'photo',)
        return super().get_readonly_fields(request, obj)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    def has_delete_permission(self, request, obj=None):
        return False

    get_html_photo.short_description = 'фото'


class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'get_html_photo', 'get_previous_html_photo', 'photo_name', 'create_at', 'updated_at',
        'moderation')
    list_filter = ('moderation', 'user')
    ordering = ('create_at', 'photo_name', 'user')
    readonly_fields = ('create_at', 'updated_at', 'previous_photo')
    search_fields = ('photo_name',)
    prepopulated_fields = {'slug': ('photo_name',)}
    exclude = ('task_id',)
    actions = ['make_published', 'make_rejected', ]

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description='Одобрено')
    def make_published(modeladmin, request, queryset):
        channel_layer = get_channel_layer()
        all_on_moderation = True
        for elem in queryset:
            if elem.moderation != "MOD":
                all_on_moderation = False
        if all_on_moderation:
            queryset.update(moderation="APR")
            for elem in queryset:
                async_to_sync(channel_layer.group_send)(
                    str(elem.user), {
                        'type': 'message',
                        'message': f"Ваше фото '{elem.photo_name}' одобрили"
                    })

    @admin.action(description='Отклонено')
    def make_rejected(modeladmin, request, queryset):
        channel_layer = get_channel_layer()
        all_on_moderation = True
        for elem in queryset:
            if elem.moderation != "MOD":
                all_on_moderation = False
        if all_on_moderation:
            queryset.update(moderation="REJ")
            for elem in queryset:
                async_to_sync(channel_layer.group_send)(
                    str(elem.user), {
                        'type': 'message',
                        'message': f"Ваше фото '{elem.photo_name}' отклонили"
                    }
                )
            DeletePhotoService.execute({'slug': elem.slug, 'user_id': elem.user.pk})

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    def get_previous_html_photo(self, object):
        if object.previous_photo:
            return mark_safe(f"<img src='{object.previous_photo.url}' width=50>")

    def get_readonly_fields(self, request, obj):
        if obj:
            if obj.moderation == "APR":
                return self.readonly_fields + ('moderation',)
        return super().get_readonly_fields(request, obj)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            kwargs['choices'] = (
                ('MOD', 'На модерации'),
                ('REJ', 'Отклоненно'),
                ('APR', 'Одобренно'),
            )
        return super(PhotoAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        channel_layer = get_channel_layer()
        if obj.moderation == 'REJ':
            try:
                async_to_sync(channel_layer.group_send)(
                    str(obj.user), {
                        'type': 'message',
                        'message': f"Ваше фото '{obj.photo_name}' отклонили"
                    }
                )
                DeletePhotoService.execute({'slug': obj.slug, 'user_id': obj.user.pk})
            except ValidationError as error:
                return HttpResponse(error)
        elif obj.moderation == 'APR':
            async_to_sync(channel_layer.group_send)(
                str(obj.user), {
                    'type': 'message',
                    'message': f"Ваше фото '{obj.photo_name}' одобрили"
                }
            )

        super().save_model(request, obj, form, change)

    get_html_photo.short_description = 'фото'
    get_previous_html_photo.short_description = 'старое фото'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('photo', 'get_html_photo', 'user', 'content', 'create_at', 'updated_at',)
    list_filter = ('photo',)
    ordering = ('create_at', 'user',)
    search_fields = ('user__username', 'content')

    def has_delete_permission(self, request, obj=None):
        return False

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

    def has_delete_permission(self, request, obj=None):
        return False

    @receiver(pre_save, sender=Like)
    def pre_save_handler(sender, instance, *args, **kwargs):
        if instance.photo.user == instance.user:
            raise Exception('It is your photo, you cant create like')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.photo.url}' width=50>")

    get_html_photo.short_description = 'фото'


admin.site.register(User, UserAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)

admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(Site)
admin.site.unregister(EmailAddress)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
# Register your models here.
