# Generated by Django 4.0.4 on 2022-06-13 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photobatle', '0002_alter_user_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Текст комментария')),
                ('date', models.DateField(verbose_name='Дата публикации')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_comment', to='photobatle.comment', verbose_name='Ребенок комментария')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_comment', to='photobatle.comment', verbose_name='Родитель комментария')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_photo', to='photobatle.photo', verbose_name='Фото')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_name_photo', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
