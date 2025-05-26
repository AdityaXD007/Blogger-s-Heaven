from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.conf import settings
from .forms import PostForm
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json


def index(request):
    return render(request, 'home/index.html')

def categories(request):
    return render(request, 'home/categories.html')

def write(request):
    return render(request, 'home/write.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.POST.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    
    # Handle GET request
    next_url = request.GET.get('next', '')
    return render(request, 'home/login.html', {'next': next_url})



def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('home')  # Redirect to homepage

    return render(request, 'home/signup.html')

def logout_view(request):
    logout(request)  # logs out on both GET and POST
    return redirect('home')


@login_required
def dashboard_view(request):
    return render(request, 'home/dashboard.html')

# Password reset
# Create your views here.

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))  # 6-digit OTP
            request.session['reset_email'] = email
            request.session['otp'] = otp
            
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
            return redirect('password_reset_otp')
        except User.DoesNotExist:
            return render(request, 'reset_password/password_reset.html', {'error': 'User not found'})
    return render(request, 'reset_password/password_reset.html')

def password_reset_otp(request):
    if request.method == "POST":
        if request.POST['otp'] == request.session.get('otp'):
            return redirect('password_reset_confirm')
        return render(request, 'reset_password/password_reset_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'reset_password/password_reset_otp.html')

def password_reset_confirm(request):
    if request.method == "POST":
        password = request.POST['password']
        email = request.session.get('reset_email')
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            request.session.flush()
            return render(request, 'reset_password/password_reset_complete.html')
        except:
            return redirect('password_reset')
    return render(request, 'reset_password/password_reset_confirm.html')

@login_required
def write_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  
            post.author = request.user     
            post.save()
            return redirect('home') 
    else:
        form = PostForm()

    return render(request, 'home/write.html', {'form': form})

# Simple in-memory storage (replace with your model)
posts_storage = []


@login_required

def write_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        category = request.POST.get('category')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if not (title and author and category and content):
            return JsonResponse({'success': False, 'message': 'Missing required fields'})

        image_url = None
        if image:
            path = default_storage.save(f"uploads/{image.name}", ContentFile(image.read()))
            image_url = settings.MEDIA_URL + path

        new_post = {
            'id': len(posts_storage) + 1,
            'title': title,
            'author': author,
            'category': category,
            'content': content,
            'date': timezone.now().strftime('%B %d, %Y'),
            'image_url': image_url or '/media/default.jpg',
        }

        posts_storage.insert(0, new_post)
        return JsonResponse({'success': True})

    return render(request, 'home/write.html')



@login_required

def categories_view(request):
    """Display all posts in categories.html"""
    # Pass posts to template as JSON for JavaScript
    posts_json = json.dumps(posts_storage)
    
    context = {
        'posts': posts_json,
        'posts_count': len(posts_storage)
    }
    
    return render(request, 'home/categories.html', context)