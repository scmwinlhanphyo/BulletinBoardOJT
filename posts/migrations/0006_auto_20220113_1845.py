# Generated by Django 3.2.10 on 2022-01-13 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20220113_1842'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='admin',
            new_name='is_staff',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='staff',
            new_name='is_superuser',
        ),
    ]
