# Generated by Django 5.1.3 on 2024-12-09 08:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentapp', '0002_alter_student_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enrollment',
            options={'verbose_name': 'Enrollment', 'verbose_name_plural': 'Enrollments'},
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentapp.student'),
        ),
    ]
