# Generated by Django 2.0.1 on 2018-02-02 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='caption',
            field=models.CharField(default='something', max_length=100),
            preserve_default=False,
        ),
    ]
