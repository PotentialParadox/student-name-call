# Generated by Django 2.2.5 on 2019-12-31 18:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='attempts',
            field=models.IntegerField(default=10, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
    ]
