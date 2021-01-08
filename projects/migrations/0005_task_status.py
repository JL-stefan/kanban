# Generated by Django 3.1.4 on 2021-01-08 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20210107_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.IntegerField(choices=[(1, '待办'), (2, '进行中'), (3, '已完成')], default=1, verbose_name='任务状态'),
        ),
    ]
