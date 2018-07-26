# Generated by Django 2.0.7 on 2018-07-16 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_auto_20180716_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceorder',
            name='status',
            field=models.CharField(choices=[('ad', 'Awaiting Delivery'), ('d', 'Delivered'), ('to', 'Not Delivered In Time'), ('ap', 'Awaiting Payment')], default='ap', max_length=3),
        ),
    ]