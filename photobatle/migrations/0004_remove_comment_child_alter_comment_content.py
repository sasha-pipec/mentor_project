# Generated by Django 4.0.4 on 2022-06-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photobatle', '0003_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='child',
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=300, verbose_name='Текст комментария'),
        ),
    ]
