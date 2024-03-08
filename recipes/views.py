from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Recipe
from .forms import IngredientSearchForm, RecipeSearchForm
import pandas as pd
from .utils import get_chart
from django.http import HttpResponse
from io import StringIO

def home(request):
    return render(request, 'recipes/home.html')

@login_required
def records(request):
    ingredient_form = IngredientSearchForm(request.POST or None)
    recipe_form = RecipeSearchForm(request.POST or None)
    ingredient_df = None
    recipe_df = None
    chart = None

    if request.method == 'POST':
        if 'ingredient_search_submit' in request.POST:
            ingredient_name = request.POST.get('ingredient_name').title()
            chart_type = request.POST.get('chart_type')

            qs = Recipe.objects.filter(ingredients__icontains=ingredient_name)
            if len(qs) > 0:
                ingredient_df = pd.DataFrame(qs.values())
                recipe_df = pd.DataFrame(qs.values())
                print('Recipe df ', recipe_df)

                ingredient_counts = qs.annotate(
                    creation_date=models.functions.TruncDate('created_at')
                ).values('creation_date').annotate(
                    count=models.Count('pk', distinct=True)
                ).order_by('creation_date')

                dates = [item['creation_date'].strftime('%m/%d/%Y') for item in ingredient_counts]
                counts = [item['count'] for item in ingredient_counts]

                counts_accumulated = []

                total_count = 0
                for item in ingredient_counts:
                    total_count += item['count']
                    counts_accumulated.append(total_count)

                counts_accumulated = [int(count) for count in counts_accumulated]
                print('TEST!!@@', str(counts_accumulated))
                print('TEST!!@@', str(counts_accumulated[0]))

                chart = get_chart(chart_type, dates, counts, ingredient_name, counts_accumulated)
        elif 'recipe_search_submit' in request.POST:
            recipe_name = request.POST.get('recipe_name').title()
            qs = Recipe.objects.filter(name__icontains=recipe_name).values('id', 'name', 'cook_time', 'ingredients', 'description', 'steps', 'image', 'created_at')
            if len(qs) > 0:
                recipe_df = pd.DataFrame(qs)
                ingredient_df = None

                for index, row in recipe_df.iterrows():
                    recipe_obj = Recipe(**row.to_dict())
                    
                    difficulty = recipe_obj.calc_difficulty()
                    recipe_df.at[index, 'difficulty'] = difficulty

                print(recipe_df)
    context = {
        'ingredient_form': ingredient_form,
        'recipe_form': recipe_form,
        'ingredient_df': ingredient_df,
        'recipe_df': recipe_df,
        'chart': chart
    }

    return render(request, 'recipes/records.html', context)



class ViewAllRecipes(ListView):
    model = Recipe
    template_name = 'recipes/all_recipes.html'

class ViewRecipeDetails(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/details.html'
