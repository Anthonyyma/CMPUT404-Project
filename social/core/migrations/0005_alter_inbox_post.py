# Generated by Django 3.2.16 on 2022-11-27 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20221127_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inbox',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.post'),
        ),
    ]