# Generated by Django 5.0.6 on 2025-01-01 07:17

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_customuser_managers_alter_customuser_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('student', 'student'), ('admin', 'admin'), ('teacher', 'teacher')], max_length=255, null=True),
        ),
    ]
