# Generated by Django 4.0.6 on 2022-08-10 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petition', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='published',
            field=models.BooleanField(default=True),
        ),
    ]
