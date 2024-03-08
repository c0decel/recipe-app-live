from io import BytesIO
import base64
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from .models import Recipe
from datetime import datetime
from collections import Counter


def get_graph():
    buffer = BytesIO()

    plt.savefig(buffer, format='png')

    buffer.seek(0)

    image_png = buffer.getvalue()

    graph = base64.b64encode(image_png)

    graph = graph.decode('utf-8')

    buffer.close()

    return graph

def get_chart(chart_type, dates, counts, ingredient_name, counts_accumulated, **kwargs):
    recipes = Recipe.objects.values('name', 'ingredients', 'created_at')

    plt.switch_backend('AGG')

    if chart_type == '#1':
        plot_bar_chart(dates, ingredient_name, counts_accumulated)
    elif chart_type == '#2':
        if recipes:
            plot_pie_chart(recipes, counts, ingredient_name, counts_accumulated)
        else:
            print('No recipe provided.')
    elif chart_type == '#3':
        plot_line_chart(dates, recipes, counts, ingredient_name, counts_accumulated)
    else:
        print('Not an option.')

    plt.tight_layout()

    chart = get_graph()
    return chart

def plot_bar_chart(dates, ingredient_name, counts_accumulated):
    fig = plt.figure(figsize=(6,3))
    plt.bar(dates, counts_accumulated)
    plt.title('How may recipes this ingredient is found in over time: ')
    plt.gcf().set_facecolor('none')

def plot_pie_chart(recipes, counts, ingredient_name, counts_accumulated):
    all_ingredients = [ingredient.title() for recipe in recipes for ingredient in recipe['ingredients'].split(', ')]

    searched_ingredient_count = counts_accumulated[-1]
    total_recipes = len(recipes)

    other_ingredients_count = total_recipes - searched_ingredient_count

    searched_percentage = round(searched_ingredient_count / total_recipes * 100, 2)
    other_percentage = round(other_ingredients_count / total_recipes * 100, 2)

    labels = [ingredient_name.title(), 'Other Ingredients']
    sizes = [searched_percentage, other_percentage]
    explode = (0.1, 0)
    custom_colors = ['#FFFFFF', '#cc002c']

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, explode=explode, colors=custom_colors)
    ax.axis('equal')
    plt.title('Percentage of recipes that this ingredient appears in vs other ingredients')
    plt.gcf().set_facecolor('none')
    plt.show()

def plot_line_chart(dates, recipes, counts, ingredient_name, counts_accumulated):
    all_ingredients = []
    creation_dates_messy = []

    for recipe in recipes:
        ingredients = [ingredient.title() for ingredient in recipe['ingredients'].split(', ')]
        all_ingredients.extend(ingredients)
        creation_dates_messy.append(recipe['created_at'])

    creation_dates = [date.strftime('%m/%d/%Y') for date in creation_dates_messy]
    unique_creation_dates = sorted(list(set(creation_dates)))

    searched_counts_per_date = []
    other_counts_per_date = []

    for date in unique_creation_dates:
        searched_count = 0
        other_count = 0
        for recipe in recipes:
            ingredients = [ingredient.title() for ingredient in recipe['ingredients'].split(', ')]
            if ingredient_name.title() in ingredients and date in recipe['created_at'].strftime('%m/%d/%Y'):
                searched_count += 1
            elif ingredient_name.title() not in ingredients and date in recipe['created_at'].strftime('%m/%d/%Y'):
                other_count += 1
        searched_counts_per_date.append(searched_count)
        other_counts_per_date.append(other_count)

    searched_counts_accumulated = [sum(searched_counts_per_date[:i+1]) for i in range(len(searched_counts_per_date))]
    other_counts_accumulated = [sum(other_counts_per_date[:i+1]) for i in range(len(other_counts_per_date))]

    print(searched_counts_accumulated)
    print(other_counts_accumulated)
    
    print(unique_creation_dates)

    fig = plt.figure(figsize=(8, 6))
    plt.plot(unique_creation_dates, searched_counts_accumulated, label=ingredient_name.title())
    plt.plot(unique_creation_dates, other_counts_accumulated, label='Other Ingredients')

    plt.xlabel('Creation Date')
    plt.ylabel('Number of Recipes')
    plt.title('Number of Recipes Over Time')
    plt.gcf().set_facecolor('none')
    plt.legend()

    plt.show()


