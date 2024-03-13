# Generated by Django 4.2.9 on 2024-03-13 05:47

from django.db import migrations, models
import recipes.models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=recipes.models.default_recipe_image, upload_to=recipes.models.recipe_image_path),
        ),
    ]
