# Generated by Django 4.2.2 on 2023-07-10 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.post'),
        ),
    ]
