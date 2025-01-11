# Generated by Django 5.0.10 on 2025-01-11 07:54

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Course Title')),
                ('description', models.TextField(verbose_name='Course Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_taught', to=settings.AUTH_USER_MODEL, verbose_name='Instructor')),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('issued_at', models.DateTimeField(auto_now_add=True, verbose_name='Issued At')),
                ('certificate_file', models.FileField(upload_to='certificates/', verbose_name='Certificate File')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to=settings.AUTH_USER_MODEL, verbose_name='Student')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='app.course', verbose_name='Course')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('enrolled_at', models.DateTimeField(auto_now_add=True, verbose_name='Enrollment Date')),
                ('completed', models.BooleanField(default=False, verbose_name='Completed')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='app.course', verbose_name='Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Module Title')),
                ('description', models.TextField(verbose_name='Module Description')),
                ('order', models.PositiveIntegerField(default=0, unique=True, verbose_name='Order')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='app.course', verbose_name='Course')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Lesson Title')),
                ('content', models.TextField(verbose_name='Lesson Content')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order')),
                ('file', models.FileField(blank=True, null=True, upload_to='lesson_files/', verbose_name='Attached File')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='app.module', verbose_name='Module')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Quiz Title')),
                ('questions', models.JSONField(null=True, verbose_name='Questions')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='app.module', verbose_name='Module')),
            ],
        ),
    ]
