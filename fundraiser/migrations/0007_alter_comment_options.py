# Generated by Django 4.0.6 on 2022-08-26 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fundraiser', '0006_comment_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created',)},
        ),
    ]