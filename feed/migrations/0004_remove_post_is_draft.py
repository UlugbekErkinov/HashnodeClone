# Generated by Django 4.0.6 on 2022-08-02 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_bookmark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_draft',
        ),
    ]
