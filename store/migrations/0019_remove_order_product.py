# Generated by Django 4.1.6 on 2023-03-29 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_alter_order_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
    ]