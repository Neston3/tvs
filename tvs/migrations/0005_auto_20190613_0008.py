# Generated by Django 2.2.1 on 2019-06-12 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvs', '0004_auto_20190516_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='full_name',
            field=models.CharField(default=12, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='users',
            name='phone_number',
            field=models.IntegerField(default=0),
        ),
    ]
