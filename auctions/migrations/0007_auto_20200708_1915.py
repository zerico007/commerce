# Generated by Django 3.0.8 on 2020-07-08 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200708_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='category',
            field=models.CharField(blank=True, choices=[('FASHION', 'Fashion'), ('TOYS', 'Toys'), ('ELECTRONIC', 'Electronic'), ('HOME', 'Home'), ('OFFICE', 'Office'), ('TOOLS', 'Tools')], max_length=100),
        ),
    ]
