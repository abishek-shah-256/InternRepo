# Generated by Django 4.2.2 on 2023-07-10 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_rename_author_post_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user_id',
            new_name='author',
        ),
    ]