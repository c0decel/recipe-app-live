# Generated by Django 4.2.9 on 2024-03-13 05:40

import datetime
from django.db import migrations, models
import recipes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('cook_time', models.FloatField(help_text='in minutes')),
                ('ingredients', models.CharField(max_length=120)),
                ('description', models.TextField(max_length=200)),
                ('steps', models.TextField(help_text='Separate each step with two commas', max_length=1000)),
                ('image', models.ImageField(default='no_img.png', upload_to=recipes.models.recipe_image_path)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2024, 1, 1, 0, 0), null=True)),
            ],
        ),
    ]