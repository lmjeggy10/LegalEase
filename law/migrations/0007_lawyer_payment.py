# Generated by Django 4.1.1 on 2023-04-20 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('law', '0006_client_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawyer',
            name='payment',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
