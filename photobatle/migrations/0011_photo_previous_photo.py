# Generated by Django 4.0.6 on 2022-08-03 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photobatle', '0010_alter_photo_moderation'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='previous_photo',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Предыдущие фото'),
        ),
    ]
