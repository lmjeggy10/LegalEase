# Generated by Django 3.2 on 2022-05-06 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('law', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawyer',
            name='exper_lowyer',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
