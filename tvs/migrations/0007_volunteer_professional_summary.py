# Generated by Django 2.2.1 on 2019-06-12 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvs', '0006_volunteer_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='professional_summary',
            field=models.TextField(default=121),
            preserve_default=False,
        ),
    ]
