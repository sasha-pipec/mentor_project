# Generated by Django 4.0.4 on 2022-07-15 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photobatle', '0008_remove_photo_like_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user_name',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='user_name',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='photo',
            old_name='user_name',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='date',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='date_published_on_site',
        ),
        migrations.AddField(
            model_name='comment',
            name='create_at',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='comment',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AddField(
            model_name='photo',
            name='create_at',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='photo',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo_name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Имя фото'),
        ),
    ]
