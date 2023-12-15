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
@csrf_exempt
def main_spa(request):
    return render(request, 'api/spa/index.html')

@csrf_exempt
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

@csrf_exempt
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


@csrf_exempt
def get_user_details(request):
    if request.user.is_authenticated:
        user_details = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'date_of_birth': request.user.date_of_birth,
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
def update_profile(request):
    try:
        user = request.user
        

        if 'profile_image' in request.FILES:
            form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                updated_user = form.save()
                return JsonResponse({'message': 'Profile updated successfully', 'file_name': updated_user.profile_image.name})
            else:
                return JsonResponse({'error': 'Invalid form data'}, status=400)
        else:
            form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
            form.save()
            return JsonResponse({'message': 'Profile updated successfully', 'file_name': user.profile_image.name})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
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
            articles = {}

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
    

   
@csrf_exempt
def all_categories(request):
    try:
        categories = Category.objects.all()

        # Create a list of category names
        category_names = [category.name for category in categories]

        return JsonResponse({'categories': category_names})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@csrf_exempt
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

@csrf_exempt
def parent_comment_list(request, article_id):
    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        # Filter comments by article_id and those with no parent_comment
        comments = Comment.objects.filter(article_id=article_id, parent_comment__isnull=True).order_by('-publication_date')
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
@csrf_exempt   
def child_comments_list(request, article_id):
    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        # Filter child comments by article_id and only include those with a parent_comment
        child_comments = Comment.objects.filter(article_id=article_id, parent_comment__isnull=False).order_by('publication_date')
        child_comments_data = {}

        # Organize child comments by parent_comment_id
        for comment in child_comments:
            parent_id = comment.parent_comment_id
            if parent_id not in child_comments_data:
                child_comments_data[parent_id] = []
            child_comments_data[parent_id].append({
                'id': comment.id,
                'content': comment.content,
                'publication_date': comment.publication_date,
                'user': comment.user.username,
                # Add more fields as needed
            })

        return JsonResponse({'child_comments': child_comments_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    if user == comment.user:
        try:
            data = json.loads(request.body)
            content = data.get('content')

            if content:
                comment.content = content
                comment.save()

                return JsonResponse({'success': True, 'comment': model_to_dict(comment)})
            
        except json.JSONDecodeError:
            print('Json Erorr')

    return JsonResponse({'success': False, 'errors': 'Invalid data'})

@login_required
@csrf_exempt
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    if user == comment.user:
        comment.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})
