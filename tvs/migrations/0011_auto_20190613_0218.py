# Generated by Django 2.2.1 on 2019-06-12 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tvs', '0010_auto_20190613_0100'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.DeleteModel(
            name='TestingModule',
        ),
    ]
