# Generated by Django 3.0.8 on 2020-07-08 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20200708_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='listing_photo',
            field=models.ImageField(blank=True, upload_to='listingPhoto'),
        ),
    ]