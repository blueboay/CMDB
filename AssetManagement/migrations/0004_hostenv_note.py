# Generated by Django 2.0.5 on 2018-05-29 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AssetManagement', '0003_hostenv'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostenv',
            name='Note',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注信息'),
        ),
    ]