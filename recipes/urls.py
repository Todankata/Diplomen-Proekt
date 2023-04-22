from django.urls import path
from . import views


urlpatterns = [
    path('', views.recipes, name='recipes'),
    path('category_slug/<slug:category_slug>/', views.recipes, name='recipes_by_category'),
    path('category_slug/<slug:category_slug>/<slug:recipe_slug>/', views.recipe_detail, name='recipe_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:recipe_id>/', views.submit_review ,name='submit_review'),

]