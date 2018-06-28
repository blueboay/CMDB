# Generated by Django 2.0.5 on 2018-06-28 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AssetManagement', '0011_auto_20180601_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=32, verbose_name='设备名称')),
                ('ManageIP', models.CharField(max_length=64, verbose_name='管理IP')),
                ('Password', models.CharField(max_length=128, verbose_name='密码')),
                ('Type', models.CharField(max_length=32, verbose_name='类型')),
                ('Brand', models.CharField(max_length=32, verbose_name='品牌')),
                ('Owner', models.CharField(max_length=32, verbose_name='所有者')),
                ('Position', models.CharField(max_length=32, verbose_name='位置')),
                ('Note', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注信息')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserName', models.CharField(max_length=32, verbose_name='用户名')),
                ('Password', models.CharField(max_length=128, verbose_name='密码')),
                ('Alias', models.CharField(max_length=32, verbose_name='别名')),
                ('PhoneNumber', models.IntegerField(blank=True, max_length=32, null=True, verbose_name='手机')),
                ('Email', models.EmailField(blank=True, max_length=32, null=True, verbose_name='邮箱')),
                ('Note', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注信息')),
            ],
        ),
    ]
