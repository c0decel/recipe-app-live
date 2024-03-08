from django.urls import path
from .views import home, records, ViewAllRecipes, ViewRecipeDetails

app_name = 'recipes'

urlpatterns = [
    path('', home),
    path('records/', records, name='records'),
    path('all_recipes/', ViewAllRecipes.as_view(), name='all_recipes'),
    path('all_recipes/<int:pk>', ViewRecipeDetails.as_view(), name='details'),
]