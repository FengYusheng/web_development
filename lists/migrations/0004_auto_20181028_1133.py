# Generated by Django 2.1.1 on 2018-10-28 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_auto_20181028_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lists.List'),
        ),
    ]
