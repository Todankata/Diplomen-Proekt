from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Recipe, ReviewRating
from category.models import Category
from django.db.models import Q
from .forms import RecipeForm

from django.core.paginator import Paginator


from .forms import ReviewForm
from django.contrib import messages
# Create your views here.

def recipes(request, category_slug=None):
    categories = None
    recipes = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        recipes = Recipe.objects.filter(category=categories)
        paginator = Paginator(recipes, 9)
        page = request.GET.get('page')
        paged_recipes = paginator.get_page(page)
        recipe_count = recipes.count()
    else:
        recipes = Recipe.objects.all().order_by('id')
        paginator = Paginator(recipes, 9)
        page = request.GET.get('page')
        paged_recipes = paginator.get_page(page)
        recipe_count = recipes.count()
    
    context ={
        'recipes': paged_recipes,
        'recipe_count': recipe_count,
    }
    return render(request, 'recipes/recipes.html', context)



def recipe_detail(request, category_slug, recipe_slug):
    try:
        single_recipe = Recipe.objects.get(category__slug=category_slug,slug=recipe_slug)
    except Exception as e:
        raise e
    
    # Get the reviews
    reviews = ReviewRating.objects.filter(recipe_id=single_recipe.id, status=True)

    context = {
        'single_recipe': single_recipe,
        'reviews': reviews,
        }
    return render(request, 'recipes/recipe_detail.html', context)

def search(request):
    if 'search' in request.GET:
        keyword = request.GET['search']
        if keyword:
            recipes = Recipe.objects.order_by('-created_date').filter(Q(recipe_name__icontains=keyword) | Q(ingredients__icontains=keyword))
            recipe_count = recipes.count()
    context = {
        'recipes': recipes,
        'recipe_count': recipe_count,
    }
    return render(request, 'recipes/recipes.html', context)

def submit_review(request, recipe_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, recipe__id=recipe_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Благодарим Ви! Ревюто ви е актуализирано.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.recipe_id = recipe_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Благодарим Ви! Вашето ревю е изпратено.')
                return redirect(url)
            
