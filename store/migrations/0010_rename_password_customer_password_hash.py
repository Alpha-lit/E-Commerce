# Generated by Django 4.1.6 on 2023-02-15 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_rename_password_hash_customer_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='password',
            new_name='password_hash',
        ),
    ]
