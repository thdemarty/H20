# Generated by Django 3.2.6 on 2021-08-23 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='ins',
            field=models.CharField(default=0, max_length=15, verbose_name='Matricule INS'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='oid',
            field=models.CharField(default=0, max_length=20, verbose_name='Object identifier'),
            preserve_default=False,
        ),
    ]