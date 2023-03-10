# Generated by Django 3.2.5 on 2021-11-16 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0002_pkeymodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='ip_addr',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='连接地址'),
        ),
        migrations.AlterField(
            model_name='host',
            name='name',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='名称/标题'),
        ),
        migrations.AlterField(
            model_name='hostcategory',
            name='name',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='名称/标题'),
        ),
        migrations.AlterField(
            model_name='pkeymodel',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
