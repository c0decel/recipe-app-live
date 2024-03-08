from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


CHART__CHOICES = (
    ('#1', 'Bar chart'),
    ('#2', 'Pie chart'),
    ('#3', 'Line chart')
)

class IngredientSearchForm(forms.Form):
    ingredient_name = forms.CharField(max_length=120, required=False)
    chart_type = forms.ChoiceField(choices=CHART__CHOICES, required=False)

class RecipeSearchForm(forms.Form):
    recipe_name = forms.CharField(max_length=120, required=False)
