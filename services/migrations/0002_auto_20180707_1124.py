# Generated by Django 2.0.7 on 2018-07-07 09:24

from django.db import migrations, models
import django.db.models.deletion
import services.models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to=services.models.get_image_path)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='images', to='services.Gallery')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceDelivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='serviceoffer',
            name='delivery_period',
            field=models.CharField(blank=True, choices=[('h', 'hours'), ('d', 'days')], default=None, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='serviceoffer',
            name='delivery_time',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='status',
            field=models.CharField(choices=[('ad', 'Awaiting Delivery'), ('d', 'Delivered'), ('to', 'Not Delivered In Time')], default='ad', max_length=3),
        ),
        migrations.AddField(
            model_name='servicedelivery',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='services.ServiceOrder'),
        ),
        migrations.AddField(
            model_name='servicedelivery',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='deliveries', to='services.ServiceOffer'),
        ),
        migrations.AddField(
            model_name='gallery',
            name='service',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='gallery', to='services.ServiceOffer'),
        ),
    ]
