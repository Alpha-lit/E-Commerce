# Generated by Django 4.1.6 on 2023-02-11 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='specifications',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]