# Generated by Django 2.2.1 on 2019-07-01 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tvs', '0012_volunteer_certificate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteer',
            name='cv',
        ),
    ]