from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import NewsArticle, Category, UserPreferences, Comment
from django.forms.models import model_to_dict
from .forms import SignUpForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages 
from django.contrib.auth import get_user_model
import json

@login_required(login_url='/login')
def main_spa(request):
    return render(request, 'api/spa/index.html')


def signup_view(request):
    form = SignUpForm()
    if request.method == 'POST':
        
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user)  
            messages.success(request, 'Signed up successfully. Please login!')
            return redirect('login')
    

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Use the default AuthenticationForm
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')  
    else: 
        form = AuthenticationForm()  # Use the default AuthenticationForm
    return render(request, 'login.html', {'form': form})

@login_required
def get_user_details(request):
    if request.user.is_authenticated:
        user_details = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'profile_image': request.user.profile_image.url if request.user.profile_image else None,
        }
        return JsonResponse(user_details)
    else:
        return JsonResponse({'error': 'User not authenticated'})


@csrf_exempt
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully. Please login to use the app!')
    
    return redirect('login')

@csrf_exempt
@login_required
def update_profile(request):
    try:
        user = request.user
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        print(user)
        if form.is_valid():
            # Generate a unique file name based on user ID
            unique_filename = f"user_{user.pk}_{form.cleaned_data['profile_image'].name}"
            
            # Set the profile_image field with the unique filename
            form.cleaned_data['profile_image'].name = unique_filename

            form.save()
            return JsonResponse({'message': 'Profile updated successfully'})
        else:
                return JsonResponse({'error': 'Invalid form data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def news_list(request):
    try:
        # Check user authentication
        user = request.user
        if not user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)

        # Get CustomUser instance
        CustomUser = get_user_model()
        custom_user = get_object_or_404(CustomUser, pk=user.pk)

        # Try to retrieve UserPreferences, return all articles if not found
        try:
            user_preferences = UserPreferences.objects.get(user=custom_user)
            favorite_categories = user_preferences.favorite_categories.all()
            articles = NewsArticle.objects.filter(category__in=favorite_categories)
        except UserPreferences.DoesNotExist:
            # Handle the case where UserPreferences does not exist for the user
            articles = NewsArticle.objects.all()

        # Prepare data with category names
        data = {
            'articles': [
                {
                    'id': article.id,
                    'title': article.title,
                    'content': article.content,
                    'publication_date': article.publication_date,
                    'category': article.category.name,  # Use category name instead of ID
                }
                for article in articles
            ]
        }

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

    #     # Retrieve UserPreferences using get_object_or_404 to handle the case when the object is not found
    #     user_preferences = get(UserPreferences, user=custom_user)
    #     favorite_categories = user_preferences.favorite_categories.values_list('id', flat=True)

    #     if not favorite_categories:
    #         # Handle the case where the user has not selected any favorite categories
    #         return JsonResponse({'articles': []})  # Return an empty list if no favorite categories

    #     articles = NewsArticle.objects.filter(category__in=favorite_categories)

    # except UserPreferences.DoesNotExist:
    #     # Handle the case where UserPreferences does not exist for the user
    #     # You can create a default UserPreferences instance for the user or take other actions
    #     articles = NewsArticle.objects.all()  # Return all articles if UserPreferences does not exist

    # return JsonResponse({'articles': list(articles.values())})

def all_categories(request):
    try:
        categories = Category.objects.all()

        # Create a list of category names
        category_names = [category.name for category in categories]

        return JsonResponse({'categories': category_names})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def user_preferences(request):
    try:
        # Check user authentication
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)
        
        # Get CustomUser instance
        CustomUser = get_user_model()
        custom_user = get_object_or_404(CustomUser, pk=user.pk)
       

        # Retrieve UserPreferences using get_object_or_404 to handle the case when the object is not found
        user_preferences = get_object_or_404(UserPreferences, user=custom_user)
        
        # Extract favorite category names from the UserPreferences
        favorite_categories = list(user_preferences.favorite_categories.values_list('name', flat=True))

        return JsonResponse({'favorite_categories': favorite_categories})

    except UserPreferences.DoesNotExist:
        # Handle the case where UserPreferences does not exist for the user
        return JsonResponse({'favorite_categories': None})

    except Exception as e:
        return JsonResponse({'favorite_categories': None})
    
@csrf_exempt
def save_user_preferences(request):
    if request.method == 'POST':
        try:

            data = json.loads(request.body)
            user = request.user

            # Get or create UserPreferences instance
            user_preferences, created = UserPreferences.objects.get_or_create(user=user)

            # Update favorite categories
            favorite_category_names = data.get('favorite_categories', [])
            favorite_categories = Category.objects.filter(name__in=favorite_category_names)
            
            # Set the favorite categories for the user
            user_preferences.favorite_categories.set(favorite_categories)

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def comment_list(request, article_id):
    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        # Order comments by publication date in descending order
        comments = Comment.objects.filter(article_id=article_id).order_by('-publication_date')
        comments_data = [
            {
                'id': comment.id,
                'content': comment.content,
                'publication_date': comment.publication_date,
                'user': comment.user.username,
                # Add more fields as needed
            }
            for comment in comments
        ]
        return JsonResponse({'comments': comments_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@login_required
def add_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')

        if title and content and category_id:
            category = Category.objects.get(pk=category_id)

            new_article = NewsArticle.objects.create(
                title=title,
                content=content,
                category=category
            )
            return JsonResponse({'success': True, 'article_id': new_article.id})
        else:
            return JsonResponse({'success': False, 'errors': 'Invalid data'})
    else:
        categories = Category.objects.all()
        return render(request, 'add_article.html', {'categories': categories})

@login_required
def article_detail(request, article_id):
    print(f"Received article_id: {article_id}")
    try:
        article = NewsArticle.objects.get(pk=article_id)
        print(f"Found article: {article}")
    except NewsArticle.DoesNotExist:
        print(f"No article found with ID: {article_id}")
    article = get_object_or_404(NewsArticle, pk=article_id)
    
    comments = Comment.objects.filter(article=article, parent_comment=None).values()

    return JsonResponse({'article': model_to_dict(article), 'comments': list(comments)})

@require_POST
@login_required
@csrf_exempt
def add_comment_to_article(request, article_id):

    article = get_object_or_404(NewsArticle, pk=article_id)
    
    try:
        data = json.loads(request.body)
        content = data.get('content')

        if content:
            new_comment = Comment.objects.create(
                content=content,
                user=request.user,
                article=article
            )

            return JsonResponse({'success': True, 'comment': model_to_dict(new_comment)})

    except json.JSONDecodeError:
        print('Json Erorr')

    return JsonResponse({'success': False, 'errors': 'Invalid data'})

@require_POST
@login_required
@csrf_exempt
def add_reply_to_comment(request, parent_comment_id):
    parent_comment = get_object_or_404(Comment, pk=parent_comment_id)
    article = parent_comment.article  
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    try:
        data = data = json.loads(request.body)
        content = data.get('content')

        if content:
            new_comment = Comment.objects.create(
                content=content,
                user=user,
                article=article,
                parent_comment=parent_comment
            )

            return JsonResponse({'success': True, 'comment': model_to_dict(new_comment)})
    except json.JSONDecodeError:
        print('Json Erorr')

    return JsonResponse({'success': False, 'errors': 'Invalid data'})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST' and request.user == comment.user:
        content = request.POST.get('content')

        if content:
            comment.content = content
            comment.save()

            return JsonResponse({'success': True, 'comment': model_to_dict(comment)})

    return JsonResponse({'success': False, 'errors': 'Invalid data'})
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST' and request.user == comment.user:
        comment.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})
