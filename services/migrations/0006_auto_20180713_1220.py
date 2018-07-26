# Generated by Django 2.0.7 on 2018-07-13 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20180710_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='service',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='services.ServiceOffer'),
        ),
        migrations.AlterField(
            model_name='image',
            name='gallery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='services.Gallery'),
        ),
        migrations.AlterField(
            model_name='servicebookmark',
            name='saved_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_services', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='servicebookmark',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='services.ServiceOffer'),
        ),
        migrations.AlterField(
            model_name='serviceinspector',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_notes', to='services.ServiceOffer'),
        ),
        migrations.AlterField(
            model_name='serviceoffer',
            name='offered_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services_offered', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='servicereview',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='services.ServiceOffer'),
        ),
    ]