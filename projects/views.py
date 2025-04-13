from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum, F, Count
from django.contrib import messages
from django.core.paginator import Paginator
from django.forms import modelformset_factory, inlineformset_factory
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from users.models import CustomUser  
# from django.db.models import Avg, Count
# from django.utils import timezone

from .forms import (
    ProjectForm, 
    ProjectImageFormSet,
    DonationForm, 
    CommentForm, 
    RatingForm,
    ProjectImageForm,
    ReportForm
)
from .models import (
    Project, 
    ProjectImage, 
    Comment, 
    Donation, 
    Rating,
    Category,
    Tag,
    Report,
)
import json
from django.db import models 
from django.db.models import Avg



@login_required
def rate_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST' and request.user != project.created_by:
        score = request.POST.get('score')
        try:
            score = int(score)
            if 1 <= score <= 5:
                # Update or create rating
                Rating.objects.update_or_create(
                    user=request.user,
                    project=project,
                    defaults={'score': score}
                )
                
                # Update project's average rating
                project.update_average_rating()
                
                return JsonResponse({
                    'success': True,
                    'new_average': project.average_rating,
                    'total_ratings': project.ratings.count()
                })
            else:
                return JsonResponse({
                    'success': False, 
                    'error': 'Rating must be between 1 and 5.'
                })
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False, 
                'error': 'Invalid rating score.'
            })
    
    return JsonResponse({
        'success': False, 
        'error': 'Invalid request'
    }, status=400)


def project_detail(request, pk):
    user_rating = None
    
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(user=request.user, project__pk=pk).score
        except Rating.DoesNotExist:
            pass

    # Get project with related data
    project = get_object_or_404(Project.objects.prefetch_related(
        'images', 'comments', 'donations'
    ).select_related('created_by'), pk=pk)

    # Get comments and ratings
    comments = project.comments.filter(parent__isnull=True).select_related('user').order_by('-created_at')
    ratings = project.ratings.all()
    average_rating = project.average_rating
    ratings_count = ratings.count()
    total_donations = project.donations.aggregate(Sum('amount'))['amount__sum'] or 0

    is_owner = request.user.is_authenticated and project.created_by == request.user

    context = {
        'project': project,
        'comments': comments,
        'average_rating': average_rating,
        'ratings_count': ratings_count,
        'total_donations': total_donations,
        'comment_form': CommentForm() if request.user.is_authenticated else None,
        'user_rating': user_rating,
        'is_owner': is_owner,
        'related_projects': project.get_related_projects(),
    }

    if messages.get_messages(request):
        context['messages'] = messages.get_messages(request)

    return render(request, 'projects/project_detail.html', context)


@login_required
def create_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        image_formset = ProjectImageFormSet(request.POST, request.FILES)

        if project_form.is_valid() and image_formset.is_valid():
            has_images = any(
                form.cleaned_data.get('image') 
                for form in image_formset.forms 
                if form.cleaned_data
            )
            
            if not has_images:
                messages.error(request, 'Please add at least one image for your project.')
            else:
                try:
                    # Save project first
                    project = project_form.save(commit=False)
                    project.created_by = request.user
                    project.save()

                    # Handle tags
                    tags_input = request.POST.get('tags_input', '').strip()
                    if tags_input:
                        tag_names = [name.strip().lower() for name in tags_input.split(',')]
                        for tag_name in tag_names:
                            if tag_name:  # Only process non-empty tags
                                tag, _ = Tag.objects.get_or_create(name=tag_name)
                                project.tags.add(tag)

                    # Save images
                    images = image_formset.save(commit=False)
                    for image in images:
                        if image.image:
                            image.project = project
                            image.save()

                    messages.success(request, 'Project created successfully!')
                    return redirect('projects:project_detail', pk=project.pk)
                except Exception as e:
                    messages.error(request, f'Error creating project: {str(e)}')
        else:
            for field, errors in project_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        project_form = ProjectForm()
        image_formset = ProjectImageFormSet(queryset=ProjectImage.objects.none())

    # Get existing tags for suggestions
    existing_tags = list(Tag.objects.values_list('name', flat=True))

    context = {
        'project_form': project_form,
        'image_formset': image_formset,
        'categories': Category.objects.all(),
        'existing_tags_json': json.dumps(existing_tags),
    }
    return render(request, 'projects/create_project.html', context)



@login_required
def donate_to_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if not project.is_active:
        messages.error(request, 'This project is not currently accepting donations.')
        return redirect('projects:project_detail', pk=project.pk)
    
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            try:
                donation = form.save(commit=False)
                donation.user = request.user
                donation.project = project
                
                if project.donated_amount + donation.amount > project.total_target:
                    messages.error(request, 'This donation would exceed the project target.')
                    return redirect('projects:project_detail', pk=project.pk)
                    
                donation.save()
                project.donated_amount = F('donated_amount') + donation.amount
                project.save(update_fields=['donated_amount'])
                project.refresh_from_db()
                
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


@login_required
def add_comment(request, pk):
    project = Project.objects.get(pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.project = project

            parent_id = request.POST.get('parent')
            if parent_id:
                try:
                    comment.parent = Comment.objects.get(id=parent_id)
                except Comment.DoesNotExist:
                    pass 

            comment.save()

            return redirect('projects:project_detail', pk=project.pk)

######################################################################################################

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk, created_by=request.user)
    
    ProjectImageFormSet = inlineformset_factory(
        Project,
        ProjectImage,
        fields=['image'],
        extra=1,
        can_delete=True,
        max_num=5,
        validate_max=True
    )

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        image_formset = ProjectImageFormSet(
            request.POST, 
            request.FILES,
            instance=project,
            prefix='form'
        )

        if project_form.is_valid() and image_formset.is_valid():
            try:
                with transaction.atomic():
                    # Save project
                    project = project_form.save()

                    # Handle tags
                    tags_input = request.POST.get('tags_input', '').strip()
                    project.tags.clear()
                    if tags_input:
                        tag_names = [name.strip() for name in tags_input.split(',') if name.strip()]
                        for tag_name in tag_names:
                            tag, _ = Tag.objects.get_or_create(name=tag_name)
                            project.tags.add(tag)

                    # Save images
                    instances = image_formset.save(commit=False)
                    for obj in image_formset.deleted_objects:
                        if obj.image:  # Check if image exists before deleting
                            obj.delete()
                    for instance in instances:
                        instance.project = project
                        instance.save()

                messages.success(request, 'Project updated successfully!')
                return redirect('projects:project_detail', pk=project.pk)
            except Exception as e:
                messages.error(request, f'Error updating project: {str(e)}')
    else:
        project_form = ProjectForm(instance=project)
        image_formset = ProjectImageFormSet(instance=project, prefix='form')

    context = {
        'project': project,
        'project_form': project_form,
        'image_formset': image_formset,
    }
    return render(request, 'projects/edit_project.html', context)

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
    projects = Project.objects.all()
    
    # Handle search
    query = request.GET.get('q', '')
    if query:
        # Using Q objects for complex queries
        projects = projects.filter(
            models.Q(title__icontains=query) |
            models.Q(tags__name__icontains=query)
        ).distinct()

    # Handle category filter
    category_id = request.GET.get('category')
    if category_id:
        projects = projects.filter(category_id=category_id)

    # Handle sorting
    sort = request.GET.get('sort', '')
    if sort == 'newest':
        projects = projects.order_by('-created_at')
    elif sort == 'most_funded':
        projects = projects.order_by('-donated_amount')
    elif sort == 'ending_soon':
        projects = projects.order_by('end_time')

    # Pagination
    paginator = Paginator(projects, 12)
    page = request.GET.get('page')
    projects = paginator.get_page(page)

    # latest projects
    limit = request.GET.get('limit')
    if limit:
        projects = projects[:int(limit)]
    
    context = {
        'projects': projects,
        'categories': Category.objects.all(),
        'search_query': query,
        'active_category': category_id,
        'active_sort': sort
    }
    return render(request, 'projects/project_list.html', context)
    
@login_required
def submit_report(request, project_id):
    if request.method == 'POST':
        report_type = request.POST.get('report_type')
        object_id = request.POST.get('object_id') 
        reason = request.POST.get('reason')

        report = Report(reporter=request.user, reason=reason, report_type=report_type)

        if report_type == 'project':
            report.project = get_object_or_404(Project, id=project_id)
        elif report_type == 'comment':
            report.comment = get_object_or_404(Comment, id=object_id)

        report.save()
        return JsonResponse({'success': True, 'message': 'Report submitted.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request.'})



def home(request):
    now = timezone.now()
    active_projects = Project.objects.filter(
        start_time__lte=now,
        end_time__gte=now
    )

    # Static testimonials data
    testimonials = [
        {
            'name': 'Mohamed Abd El-Hay',
            'role': 'Regular Donor',
            'content': 'I\'ve supported multiple projects through this platform. It\'s amazing to see the direct impact of my contributions!',
            'image': 'images/testimonials/donor1.jpg',
            'rating': 5,
            'donated': '55,000 EGP',
            'projects': 12
        },
        {
            'name': 'Sarah Wilson',
            'role': 'Project Creator',
            'content': 'This platform made it easy to bring my project to life. The community here is incredibly supportive.',
            'image': 'images/testimonials/creator1.jpg',
            'rating': 5,
            'donated': '15,000 EGP',
            'projects': 8
        },
        {
            'name': 'Hazem Khaled',
            'role': 'Tech Enthusiast',
            'content': 'The transparency and ease of use make this platform stand out. I love tracking the progress of projects I support.',
            'image': 'images/testimonials/donor2.jpg',
            'rating': 4,
            'donated': '30,000 EGP',
            'projects': 15
        }
    ]

    # Get top donors
    top_donors = CustomUser.objects.annotate(
        total_donated=Sum('donation__amount'),
        projects_supported=Count('donation__project', distinct=True)
    ).filter(
        total_donated__gt=0
    ).order_by('-total_donated')[:3]


    # Handle search
    search_query = request.GET.get('q', '')
    category_id = request.GET.get('category')

    # Filter projects based on search and category
    filtered_projects = active_projects
    if search_query:
        filtered_projects = filtered_projects.filter(
            models.Q(title__icontains=search_query) |
            models.Q(tags__name__icontains=search_query)
        ).distinct()
        
    # Update category filtering logic
    if category_id and category_id != 'all':
        try:
            category_id = int(category_id)
            filtered_projects = filtered_projects.filter(category_id=category_id)
            active_category_name = Category.objects.get(id=category_id).name
        except (ValueError, Category.DoesNotExist):
            category_id = None
            active_category_name = None
    else:
        category_id = None
        active_category_name = None


    # Get overall statistics
    total_projects = Project.objects.count()
    total_donors = CustomUser.objects.filter(donation__isnull=False).distinct().count()
    total_donated = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'top_rated_projects': active_projects.annotate(
            avg_rating=Avg('ratings__score')
        ).filter(
            avg_rating__isnull=False
        ).order_by('-avg_rating')[:5],
        
        'latest_projects': active_projects.order_by(
            '-created_at'
        )[:5],
        
        'featured_projects': active_projects.filter(
            is_featured=True
        )[:5],
        
        'categories': Category.objects.annotate(
            projects_count=Count('projects')
        ).order_by('-projects_count'),
        
        'projects': filtered_projects,  
        'search_query': search_query,
        'active_category': category_id,
        'active_category_name': active_category_name,
        'top_donors': top_donors,
        'total_projects': total_projects,
        'total_donors': total_donors,
        'total_donated': total_donated,
        'testimonials': testimonials
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        template = 'projects/components/project_list_partial.html'
    else:
        template = 'home.html'

    return render(request, template, context)