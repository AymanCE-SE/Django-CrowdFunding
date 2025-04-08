from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum, F
from django.contrib import messages
from django.core.paginator import Paginator
from django.forms import modelformset_factory  
from .forms import (
    ProjectForm, 
    ProjectImageFormSet,
    DonationForm, 
    CommentForm, 
    RatingForm,
    ProjectImageForm
)
from .models import (
    Project, 
    ProjectImage, 
    Comment, 
    Donation, 
    Rating,
    Category,
    Tag
)
import json


##########################################################################



def project_detail(request, pk):
    try:
        # Get project with related data
        project = get_object_or_404(Project.objects.prefetch_related(
            'images', 'comments', 'donations'
        ).select_related('created_by'), pk=pk)
        
        # Get comments and ratings
        comments = project.comments.select_related('user').order_by('-created_at')
        ratings = project.ratings.all()
        average_rating = ratings.aggregate(Avg('score'))['score__avg']
        total_donations = project.donations.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Get project owner status for template
        is_owner = request.user.is_authenticated and project.created_by == request.user
        
        context = {
            'project': project,
            'comments': comments,
            'average_rating': average_rating,
            'total_donations': total_donations,
            'comment_form': CommentForm() if request.user.is_authenticated else None,
            'is_owner': is_owner,
        }
        
        # Add any messages to the context
        if messages.get_messages(request):
            context['messages'] = messages.get_messages(request)
            
        return render(request, 'projects/project_detail.html', context)
        
    except Exception as e:
        messages.error(request, f"Error loading project: {str(e)}")
        return redirect('projects:project_list')


##############################################################################################################
@login_required
def create_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        image_formset = ProjectImageFormSet(request.POST, request.FILES)

        if project_form.is_valid() and image_formset.is_valid():
            # Check if at least one image was uploaded
            has_images = any(
                form.cleaned_data.get('image') 
                for form in image_formset.forms 
                if form.cleaned_data
            )
            
            if not has_images:
                messages.error(request, 'Please add at least one image for your project.')
            else:
                try:
                    project = project_form.save(commit=False)
                    project.created_by = request.user
                    project.save()
                    project_form.save_m2m()

                    # Save images
                    images = image_formset.save(commit=False)
                    for image in images:
                        if image.image:  # Only save image if it exists
                            image.project = project
                            image.save()

                    messages.success(request, 'Project created successfully!')
                    return redirect('projects:project_detail', pk=project.pk)
                except Exception as e:
                    messages.error(request, f'Error creating project: {str(e)}')
        else:
            # Show form errors
            for field, errors in project_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        project_form = ProjectForm()
        image_formset = ProjectImageFormSet(queryset=ProjectImage.objects.none())  # No images to pre-load

    context = {
        'project_form': project_form,
        'image_formset': image_formset,
        'categories': Category.objects.all(),
        'existing_tags_json': json.dumps(list(Tag.objects.values_list('name', flat=True))),
    }
    return render(request, 'projects/create_project.html', context)


############################################################################################

@login_required
def donate_to_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    # Check if project is active for donations
    try:
        is_active = project.is_active()  # Store the result
    except Exception as e:
        messages.error(request, 'Error checking project status.')
        return redirect('projects:project_detail', pk=project.pk)
    
    if not is_active:  # Use the stored result
        messages.error(request, 'This project is not currently accepting donations.')
        return redirect('projects:project_detail', pk=project.pk)
    
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            try:
                donation = form.save(commit=False)
                donation.user = request.user
                donation.project = project
                
                # Check if donation would exceed target
                if project.donated_amount + donation.amount > project.total_target:
                    messages.error(request, 'This donation would exceed the project target.')
                    return redirect('projects:project_detail', pk=project.pk)
                    
                donation.save()
                project.donated_amount = F('donated_amount') + donation.amount
                project.save()
                
                messages.success(request, 'Thank you for your donation!')
                return redirect('projects:project_detail', pk=project.pk)
            except Exception as e:
                messages.error(request, f'Error processing donation: {str(e)}')
                return redirect('projects:project_detail', pk=project.pk)
    else:
        form = DonationForm()
    
    return render(request, 'projects/donate_to_project.html', {
        'form': form,
        'project': project
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
            score = form.cleaned_data['score']
            rating, created = Rating.objects.get_or_create(
                user=request.user,
                project=project,
                defaults={'score': score}  # Set initial score for new ratings
            )
            if not created:
                rating.score = score  # Update score for existing ratings
                rating.save()

            return redirect('projects:project_detail', pk=project.pk)
    else:
        # Pre-populate form with existing rating if it exists
        try:
            existing_rating = Rating.objects.get(user=request.user, project=project)
            form = RatingForm(initial={'score': existing_rating.score})
        except Rating.DoesNotExist:
            form = RatingForm()

    return render(request, 'projects/rate_project.html', {
        'form': form,
        'project': project,
    })
##############################################################################################################


@login_required
@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.created_by != request.user:
        messages.error(request, "You don't have permission to edit this project.")
        return redirect('projects:project_detail', pk=project.pk)

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, request.FILES, instance=project)
        ImageFormSet = modelformset_factory(ProjectImage, form=ProjectImageForm, extra=0, can_delete=True)
        image_formset = ImageFormSet(request.POST, request.FILES, queryset=ProjectImage.objects.filter(project=project))

        if project_form.is_valid() and image_formset.is_valid():
            try:
                # Save project changes
                project = project_form.save()

                # Save new images and handle deletions
                images = image_formset.save(commit=False)
                for image in images:
                    image.project = project
                    image.save()

                # Delete images marked for deletion
                for obj in image_formset.deleted_objects:
                    obj.delete()

                messages.success(request, 'Project updated successfully!')
                return redirect('projects:project_detail', pk=project.pk)

            except Exception as e:
                messages.error(request, f'Error updating project: {str(e)}')
        else:
            print("Project Form Errors:", project_form.errors)
            print("Image Formset Errors:", image_formset.errors)

    else:
        project_form = ProjectForm(instance=project)
        ImageFormSet = modelformset_factory(ProjectImage, form=ProjectImageForm, extra=0, can_delete=True)
        image_formset = ImageFormSet(queryset=ProjectImage.objects.filter(project=project))

    return render(request, 'projects/edit_project.html', {
        'project_form': project_form,
        'image_formset': image_formset,
        'project': project,
    })

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    # Check if user is the project creator
    if not project.is_owner(request.user):
        messages.error(request, "You don't have permission to delete this project.")
        return redirect('projects:project_detail', pk=project.pk)
    
    # Check if project can be deleted
    if not project.can_be_deleted():
        messages.error(request, 
            f"Cannot delete project. Current donations ({project.get_donation_percentage():.1f}%) exceed 25% of target amount.")
        return redirect('projects:project_detail', pk=project.pk)
    
    if request.method == 'POST':
        try:
            project.delete()
            messages.success(request, 'Project deleted successfully!')
            return redirect('projects:project_list')
        except Exception as e:
            messages.error(request, f'Error deleting project: {str(e)}')
            return redirect('projects:project_detail', pk=project.pk)
            
    return render(request, 'projects/delete_project.html', {
        'project': project,
        'donation_percentage': project.get_donation_percentage()
    })


def project_list(request):
    projects = Project.objects.all().prefetch_related('images').order_by('-created_at')
    paginator = Paginator(projects, 12)
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    
    return render(request, 'projects/project_list.html', {
        'projects': projects,
        'categories': Category.objects.all(),
    })