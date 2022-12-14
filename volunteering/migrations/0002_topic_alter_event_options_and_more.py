# Generated by Django 4.0.6 on 2022-08-14 19:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('start_date',)},
        ),
        migrations.RenameField(
            model_name='event',
            old_name='cerated',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='date',
            new_name='end_date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='category',
        ),
        migrations.RemoveField(
            model_name='event',
            name='location',
        ),
        migrations.AddField(
            model_name='event',
            name='arrangements',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='country',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='deadline',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='participant_profile',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='street',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='training',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AddField(
            model_name='topic',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='topics', to='volunteering.event'),
        ),
    ]
