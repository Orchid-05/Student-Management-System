# Generated by Django 5.1.3 on 2024-12-09 08:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentapp', '0005_alter_enrollment_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentapp.student'),
        ),
    ]
