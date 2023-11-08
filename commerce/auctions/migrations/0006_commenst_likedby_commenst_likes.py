# Generated by Django 4.2.1 on 2023-08-17 15:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_commenst_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='commenst',
            name='likedBy',
            field=models.ManyToManyField(null=True, related_name='liked_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commenst',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]