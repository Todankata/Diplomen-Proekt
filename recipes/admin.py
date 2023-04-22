
from django.contrib import admin
from .models import Recipe, ReviewRating


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe_name', 'category', 'modified_date', 'preparation', 'cook', 'yields')
    search_fields = ('recipe_name', 'category', 'preparation', 'cook', 'yields')
    prepopulated_fields = {'slug': ('recipe_name',)}

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'subject', 'status')
    list_filter = ('status', 'updated_at')
    search_fields = ('review', 'subject', 'recipe__recipe_name')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)