# Generated by Django 4.2.1 on 2023-11-06 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_alter_user_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
