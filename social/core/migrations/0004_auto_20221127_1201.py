# Generated by Django 3.2.16 on 2022-11-27 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_comment_external_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='external_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='github',
            field=models.URLField(blank=True, null=True),
        ),
    ]
