from django.test import TestCase
from django.urls import reverse
from .models import Recipe
from users.models import User
from .forms import IngredientSearchForm
from .views import records
import unittest
from io import BytesIO
from matplotlib import pyplot as plt
from .utils import get_graph, plot_bar_chart, plot_pie_chart, plot_line_chart


class RecipeModelTest(TestCase):

    def setUpTestData():
        Recipe.objects.create(name='Tea', cook_time=5, ingredients='tea leaves, water, sugar', description='Steep tea leaves in boiling water and add sugar.', steps='Boil water,, Add tea leaves,, Add sugar')

    def test_name(self):
        recipe = Recipe.objects.get(id=1)
        recipe_name = recipe._meta.get_field('name').verbose_name
        self.assertEqual(recipe_name, 'name')

    def test_cook_time(self):
        recipe = Recipe.objects.get(id=1)
        recipe_cook_time = recipe._meta.get_field('cook_time').help_text
        self.assertEqual(recipe_cook_time, 'in minutes')
        
    def test_calc_difficulty(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.calc_difficulty(), 'Easy')

    def test_steps(self):
        recipe = Recipe.objects.get(id=1)
        recipe_steps = recipe._meta.get_field('steps').help_text
        self.assertEqual(recipe_steps, 'Separate each step with two commas')

    def test_steps_to_list(self):
        recipe = Recipe.objects.get(id=1)
        expected_steps = ['1. Boil water', '2. Add tea leaves', '3. Add sugar']
        self.assertEqual(recipe.steps_to_list(), expected_steps)

class RecordsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='testpassword')
        Recipe.objects.create(name='Test Recipe', cook_time=30, ingredients='Ingredient 1, Ingredient 2', description='Test description', steps='Step 1, Step 2', created_at='2024-01-01')

    def test_records_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('recipes:records'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'recipes/records.html')

        self.assertIn('ingredient_form', response.context)

        self.assertIn('ingredient_df', response.context)

        self.assertIn('recipe_df', response.context)

    def test_records_view_with_unauthenticated_user(self):
        response = self.client.get(reverse('recipes:records'))

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, '/login/?next=/records/')