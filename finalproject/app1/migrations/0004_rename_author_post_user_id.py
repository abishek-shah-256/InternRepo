# Generated by Django 4.2.2 on 2023-07-10 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_rename_user_id_post_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='author',
            new_name='user_id',
        ),
    ]