from django.db import models
from category.models import Category
from accounts.models import Account
from django.db.models import Avg, Count

from django.urls import reverse

# Create your models here.

class Recipe(models.Model):
    recipe_name     = models.CharField(max_length=50, unique=True)
    slug            = models.SlugField(max_length=50, unique=True)
    description     = models.TextField(max_length=300, blank=True)
    ingredients     = models.TextField(blank=True)
    preparation     = models.IntegerField(blank=True)
    cook            = models.IntegerField(blank=True)
    yields          = models.IntegerField(blank=True)
    images          = models.ImageField(upload_to='photos/recipes')
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by      = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='recipes_created')
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('recipe_detail', args=[self.category.slug, self.slug])
        
    def __str__(self):
        return self.recipe_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(recipe=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(recipe=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class ReviewRating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    review = models.TextField(max_length=500)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
