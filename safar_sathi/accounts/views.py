from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser, LocalGuide
from .forms import SignUpForm, ProfileUpdateForm, GuideForm
from reviews.models import GuideReview

def staff_required(user):
    return user.is_staff

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Safar Sathi.')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

class GuideListView(ListView):
    model = LocalGuide
    template_name = 'accounts/guide_list.html'
    context_object_name = 'guides'
    paginate_by = 9

def guide_detail_view(request, pk):
    guide = get_object_or_404(LocalGuide, pk=pk)
    reviews = GuideReview.objects.filter(guide=guide).select_related('user').prefetch_related('photos')[:5]
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = GuideReview.objects.filter(guide=guide, user=request.user).exists()
    return render(request, 'accounts/guide_detail.html', {
        'guide': guide,
        'reviews': reviews,
        'user_has_reviewed': user_has_reviewed,
    })

@user_passes_test(staff_required)
def guide_create_view(request):
    if request.method == 'POST':
        form = GuideForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = CustomUser.objects.create_user(
                    username=form.cleaned_data['user_username'],
                    email=form.cleaned_data['user_email'],
                    first_name=form.cleaned_data['user_first_name'],
                    last_name=form.cleaned_data['user_last_name'],
                    password='SafarSathi@2025'
                )
                guide = form.save(commit=False)
                guide.user = user
                guide.save()
                messages.success(request, 'Guide created successfully!')
                return redirect('accounts:guide_detail', pk=guide.pk)
            except Exception as e:
                messages.error(request, f'Error: {e}')
    else:
        form = GuideForm()
    return render(request, 'accounts/guide_form.html', {'form': form, 'title': 'Create Guide'})

@user_passes_test(staff_required)
def guide_update_view(request, pk):
    guide = get_object_or_404(LocalGuide, pk=pk)
    if request.method == 'POST':
        form = GuideForm(request.POST, request.FILES, instance=guide)
        if form.is_valid():
            guide.user.first_name = form.cleaned_data['user_first_name']
            guide.user.last_name = form.cleaned_data['user_last_name']
            guide.user.username = form.cleaned_data['user_username']
            guide.user.email = form.cleaned_data['user_email']
            guide.user.save()
            form.save()
            messages.success(request, 'Guide updated successfully!')
            return redirect('accounts:guide_detail', pk=guide.pk)
    else:
        form = GuideForm(instance=guide)
    return render(request, 'accounts/guide_form.html', {'form': form, 'title': 'Edit Guide'})

@user_passes_test(staff_required)
def guide_delete_view(request, pk):
    guide = get_object_or_404(LocalGuide, pk=pk)
    if request.method == 'POST':
        guide.user.delete()
        messages.success(request, 'Guide deleted successfully.')
        return redirect('accounts:guide_list')
    return render(request, 'accounts/guide_confirm_delete.html', {'guide': guide})
