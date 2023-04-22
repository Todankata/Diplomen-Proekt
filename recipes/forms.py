from django import forms
from .models import ReviewRating, Recipe

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_name', 'description', 'ingredients', 'preparation', 'cook', 'yields', 'category', 'images']
