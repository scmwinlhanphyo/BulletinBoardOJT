# Generated by Django 3.2.10 on 2022-01-25 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20220125_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.FileField(default='/user_default.png', null=True, upload_to='', verbose_name=''),
        ),
    ]
