# Generated by Django 5.0.6 on 2025-01-02 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_studentanswer_quiz_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='questions',
            field=models.JSONField(null=True, verbose_name='Questions'),
        ),
    ]
