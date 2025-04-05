from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import ProjectForm, ProjectImageFormSet
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectImage
from .forms import DonationForm
from django.shortcuts import render, get_object_or_404
from .models import Project, Comment, Donation, Rating
from django.db.models import Avg, Sum


##########################################################################



def project_detail(request, pk):
    # Get the project object or return 404 if not found
    project = get_object_or_404(Project, pk=pk)
    
    # Get all comments related to the project
    comments = project.comments.all()
    
    # Get all ratings related to the project
    ratings = project.ratings.all()
    
    # Calculate average rating for the project
    average_rating = ratings.aggregate(Avg('score'))['score__avg'] if ratings else None
    
    # Calculate total donations for the project
    total_donations = project.donations.aggregate(Sum('amount'))['amount__sum'] or 0

    # Pass the data to the template
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'comments': comments,
        'average_rating': average_rating,
        'total_donations': total_donations,
    })


##############################################################################################################
@login_required
def create_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, request.FILES)
        image_formset = ProjectImageFormSet(request.POST, request.FILES)

        if project_form.is_valid() and image_formset.is_valid():
            project = project_form.save(commit=False)
            project.created_by = request.user  # Assign current user as creator
            project.save()

            # Save images
            for form in image_formset:
                image = form.save(commit=False)
                image.project = project
                image.save()

            return redirect('projects:project_detail', pk=project.pk)
    else:
        project_form = ProjectForm()
        image_formset = ProjectImageFormSet(queryset=ProjectImage.objects.none())

    return render(request, 'projects/create_project.html', {
        'project_form': project_form,
        'image_formset': image_formset,
    })


############################################################################################

@login_required
def donate_to_project(request, pk):
    project = Project.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = DonationForm(request.POST)
        
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user
            donation.project = project
            donation.save()

            # Update the project's total donation
            project.donated_amount += donation.amount
            project.save()

            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = DonationForm()

    return render(request, 'projects/donate_to_project.html', {
        'form': form,
        'project': project,
    })


#############################################################################################

@login_required
def add_comment(request, pk):
    project = Project.objects.get(pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.project = project
            comment.save()

            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = CommentForm()

    return render(request, 'projects/add_comment.html', {
        'form': form,
        'project': project,
    })
######################################################################################################

@login_required
def rate_project(request, pk):
    project = Project.objects.get(pk=pk)

    if request.method == 'POST':
        form = RatingForm(request.POST)

        if form.is_valid():
            rating, created = Rating.objects.get_or_create(
                user=request.user,
                project=project
            )
            rating.score = form.cleaned_data['score']
            rating.save()

            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = RatingForm()

    return render(request, 'projects/rate_project.html', {
        'form': form,
        'project': project,
    })
##############################################################################################################


from django.shortcuts import render
from .models import Project 
def project_list(request):
    projects = Project.objects.all()  
    return render(request, 'projects/project_list.html', {'projects': projects})