# Generated by Django 2.0.5 on 2018-05-29 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AssetManagement', '0002_auto_20180525_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostENV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EnvName', models.CharField(max_length=32, verbose_name='环境名称')),
            ],
        ),
    ]
