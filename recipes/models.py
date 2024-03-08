from django.db import models
from django.urls import reverse
from datetime import datetime
from django.utils import timezone


class Recipe(models.Model):
    name = models.CharField(max_length=50)
    cook_time = models.FloatField(help_text='in minutes')
    ingredients = models.CharField(max_length=120)
    description = models.TextField(max_length=200)
    steps = models.TextField(max_length=1000, help_text='Separate each step with two commas')
    image = models.ImageField(upload_to='recipe_images', default='no_img.PNG')
    created_at = models.DateTimeField(blank=True, null=True, default=datetime(2024, 1, 1))

    def calc_difficulty(self):
        ingredients = self.ingredients.split(', ')
        if self.cook_time < 10 and len(ingredients) < 4:
            self.difficulty = 'Easy'
        elif self.cook_time < 10 and len(ingredients) >= 4:
            self.difficulty = 'Medium'
        elif self.cook_time >= 10 and len(ingredients) < 4:
            self.difficulty = 'Intermediate'
        else:
            self.difficulty = 'Hard'
        return self.difficulty

    def __str__(self):
        return str(self.name)

    def ingredients_to_list(self):
        ingredients_list = self.ingredients.split(',')
        return ingredients_list

    def steps_to_list(self):
        steps_list = self.steps.split(',, ')
        numbered_steps = []
        for index, item in enumerate(steps_list):
            numbered_item = f'{index + 1}. {item}'
            numbered_steps.append(numbered_item)
        return numbered_steps

    def get_absolute_url(self):
        return reverse('recipes:details', kwargs={'pk': self.pk})
