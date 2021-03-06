# Generated by Django 2.1.8 on 2019-07-28 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0002_auto_20190725_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_id', models.IntegerField(max_length=32, verbose_name='商品id')),
                ('goods_name', models.CharField(max_length=32, verbose_name='商品名称')),
                ('goods_price', models.FloatField(max_length=32, verbose_name='商品价格')),
                ('goods_picture', models.ImageField(upload_to='', verbose_name='商品图片')),
                ('goods_num', models.IntegerField(max_length=32, verbose_name='商品数量')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Buyer')),
            ],
        ),
    ]
