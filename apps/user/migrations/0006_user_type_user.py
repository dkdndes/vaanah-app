# Generated by Django 3.1.7 on 2021-04-19 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210414_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type_user',
            field=models.CharField(choices=[('Customer', 'Customer'), ('Seller', 'Seller')], default='Customer', max_length=20),
        ),
    ]