# Generated by Django 4.2.2 on 2023-07-13 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='status',
            field=models.CharField(choices=[('send', 'send'), ('accepted', 'accepted'), ('waiting', 'waiting'), ('rejected', 'rejected')], max_length=15),
        ),
    ]