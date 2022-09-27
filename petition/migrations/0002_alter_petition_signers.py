# Generated by Django 4.0.6 on 2022-08-09 21:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('petition', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='signers',
            field=models.ManyToManyField(blank=True, related_name='petitions', to=settings.AUTH_USER_MODEL),
        ),
    ]