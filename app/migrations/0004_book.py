# Generated by Django 4.1.3 on 2022-11-27 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_readertype_punish_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, verbose_name='书号')),
                ('name', models.CharField(max_length=255, verbose_name='书名')),
                ('authors', models.CharField(max_length=255, verbose_name='作者')),
                ('publisher', models.CharField(max_length=255, verbose_name='出版社')),
                ('publish_time', models.DateTimeField(verbose_name='出版日期')),
                ('isbn', models.CharField(max_length=255, verbose_name='ISBN')),
                ('catalog', models.CharField(max_length=255, verbose_name='分类号')),
                ('language', models.CharField(choices=[(1, '中文'), (2, '英文'), (3, '日文'), (4, '俄文'), (5, '德文'), (6, '法文'), (99, '其他')], max_length=2, null=True, verbose_name='语言')),
                ('total_pages', models.IntegerField(verbose_name='总页数')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价格')),
            ],
        ),
    ]
