# Generated by Django 3.1.7 on 2021-08-16 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_post_editmode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='editMode',
            field=models.BooleanField(default=False),
        ),
    ]
