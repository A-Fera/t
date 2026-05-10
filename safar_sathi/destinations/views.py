from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView
from .models import Destination, Photo
from .forms import DestinationForm, PhotoUploadForm
from reviews.models import DestinationReview
from bookings.models import Accommodation

def staff_required(user):
    return user.is_staff

class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'
    paginate_by = 9

    def get_queryset(self):
        qs = Destination.objects.all()
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        if search:
            qs = qs.filter(name__icontains=search) | qs.filter(location__icontains=search)
        if category:
            qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Destination.CATEGORY_CHOICES
        ctx['search'] = self.request.GET.get('search', '')
        ctx['selected_category'] = self.request.GET.get('category', '')
        return ctx

def destination_detail_view(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    photos = destination.photos.all()
    reviews = DestinationReview.objects.filter(destination=destination).select_related('user').prefetch_related('photos')[:5]
    accommodations = Accommodation.objects.filter(destination=destination)[:5]
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = DestinationReview.objects.filter(destination=destination, user=request.user).exists()
    return render(request, 'destinations/destination_detail.html', {
        'destination': destination,
        'photos': photos,
        'reviews': reviews,
        'accommodations': accommodations,
        'user_has_reviewed': user_has_reviewed,
    })

@user_passes_test(staff_required)
def destination_create_view(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST)
        if form.is_valid():
            dest = form.save(commit=False)
            dest.created_by = request.user
            dest.save()
            messages.success(request, 'Destination created!')
            return redirect('destinations:destination_detail', pk=dest.pk)
    else:
        form = DestinationForm()
    return render(request, 'destinations/destination_form.html', {'form': form, 'title': 'Add Destination'})

@user_passes_test(staff_required)
def destination_update_view(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationForm(request.POST, instance=destination)
        if form.is_valid():
            form.save()
            messages.success(request, 'Destination updated!')
            return redirect('destinations:destination_detail', pk=destination.pk)
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'destinations/destination_form.html', {'form': form, 'title': 'Edit Destination'})

@user_passes_test(staff_required)
def destination_delete_view(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.delete()
        messages.success(request, 'Destination deleted.')
        return redirect('destinations:destination_list')
    return render(request, 'destinations/destination_confirm_delete.html', {'destination': destination})

@login_required
def photo_upload_view(request, destination_pk):
    destination = get_object_or_404(Destination, pk=destination_pk)
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.destination = destination
            photo.user = request.user
            photo.save()
            messages.success(request, 'Photo uploaded!')
            return redirect('destinations:destination_detail', pk=destination.pk)
    else:
        form = PhotoUploadForm()
    return render(request, 'destinations/photo_upload.html', {'form': form, 'destination': destination})
