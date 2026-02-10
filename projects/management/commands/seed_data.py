from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from projects.models import Category, Tag, Project, ProjectImage, Donation, Rating, Comment
from users.models import Profile
from datetime import timedelta
from decimal import Decimal
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import requests
import random
import io
from PIL import Image as PILImage, ImageDraw

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with realistic test data for all features'

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('Starting data seeding...'))
        
        try:
            # Clear existing data (optional)
            # User.objects.all().delete()
            # Category.objects.all().delete()
            # Tag.objects.all().delete()
            
            # Create categories
            self.stdout.write('Creating categories...')
            categories = self.create_categories()
            
            # Create tags
            self.stdout.write('Creating tags...')
            tags = self.create_tags()
            
            # Create users
            self.stdout.write('Creating users...')
            users = self.create_users()
            
            # Create projects
            self.stdout.write('Creating projects...')
            projects = self.create_projects(users, categories, tags)
            
            # Create donations
            self.stdout.write('Creating donations...')
            self.create_donations(users, projects)
            
            # Create ratings
            self.stdout.write('Creating ratings...')
            self.create_ratings(users, projects)
            
            # Create comments
            self.stdout.write('Creating comments...')
            self.create_comments(users, projects)
            
            self.stdout.write(self.style.SUCCESS('✓ Data seeding completed successfully!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error during seeding: {str(e)}'))
            raise

    def create_categories(self):
        """Create project categories"""
        categories_data = [
            {'name': 'Technology'},
            {'name': 'Education'},
            {'name': 'Health & Medicine'},
            {'name': 'Arts & Culture'},
            {'name': 'Environment'},
            {'name': 'Social Impact'},
            {'name': 'Business'},
            {'name': 'Community'},
        ]
        
        categories = []
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(**cat_data)
            if created:
                self.stdout.write(f'  ✓ Created category: {cat.name}')
            categories.append(cat)
        return categories

    def create_tags(self):
        """Create project tags"""
        tags_data = [
            'Innovative', 'Eco-Friendly', 'Community-Driven', 'Educational',
            'Healthcare', 'Sustainable', 'AI & Technology', 'Social Justice',
            'Small Business', 'Green Energy', 'Mental Health', 'Women Empowerment',
            'Youth Program', 'Research', 'Open Source', 'Startup'
        ]
        
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(f'  ✓ Created tag: {tag.name}')
            tags.append(tag)
        return tags

    def create_users(self):
        """Create test users with profiles"""
        users_data = [
            {
                'username': 'ahmed_tech',
                'email': 'ahmed@example.com',
                'first_name': 'Ahmed',
                'last_name': 'Hassan',
                'phone_number': '01001234567',
                'profile': {
                    'country': 'Egypt',
                    'bio': 'Tech enthusiast and co-founder of innovative startups',
                }
            },
            {
                'username': 'fatima_health',
                'email': 'fatima@example.com',
                'first_name': 'Fatima',
                'last_name': 'Ahmed',
                'phone_number': '01101234567',
                'profile': {
                    'country': 'Egypt',
                    'bio': 'Healthcare professional passionate about community wellbeing',
                }
            },
            {
                'username': 'mahmoud_arts',
                'email': 'mahmoud@example.com',
                'first_name': 'Mahmoud',
                'last_name': 'Ibrahim',
                'phone_number': '01201234567',
                'profile': {
                    'country': 'Egypt',
                    'bio': 'Artist and cultural advocate supporting local talents',
                }
            },
            {
                'username': 'layla_env',
                'email': 'layla@example.com',
                'first_name': 'Layla',
                'last_name': 'Mohamed',
                'phone_number': '01501234567',
                'profile': {
                    'country': 'Egypt',
                    'bio': 'Environmental activist focused on sustainable solutions',
                }
            },
            {
                'username': 'sara_education',
                'email': 'sara@example.com',
                'first_name': 'Sara',
                'last_name': 'Ali',
                'phone_number': '01051234567',
                'profile': {
                    'country': 'Egypt',
                    'bio': 'Educator committed to making quality education accessible',
                }
            },
            {
                'username': 'karim_social',
                'email': 'karim@example.com',
                'first_name': 'Karim',
                'last_name': 'Saleh',
                'phone_number': '01251234567',
                'profile': {
                    'country': 'Egypt',
                    'bio': 'Social entrepreneur working on poverty alleviation programs',
                }
            },
            {
                'username': 'amira_business',
                'email': 'amira@example.com',
                'first_name': 'Amira',
                'last_name': 'Karim',
                'phone_number': '01151234567',
                'profile': {
                    'country': 'Egypt',
                    'bio': 'Business consultant helping small businesses succeed',
                }
            },
            {
                'username': 'hassan_investor',
                'email': 'hassan@example.com',
                'first_name': 'Hassan',
                'last_name': 'Omar',
                'phone_number': '01351234567',
                'profile': {
                    'country': 'Egypt',
                    'bio': 'Angel investor supporting innovative startups',
                }
            },
        ]
        
        users = []
        for user_data in users_data:
            profile_data = user_data.pop('profile', {})
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={**user_data, 'is_active': True}
            )
            if created:
                self.stdout.write(f'  ✓ Created user: {user.get_full_name()} ({user.username})')
                # Update profile with data and add profile picture
                profile = user.profile
                for key, value in profile_data.items():
                    setattr(profile, key, value)
                
                # Add profile picture from online source
                try:
                    profile_pic_url = self.get_random_profile_picture()
                    profile.profile_picture = profile_pic_url
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  ⚠ Could not set profile picture for {user.get_full_name()}: {str(e)}'))
                
                profile.save()
            users.append(user)
        return users

    def create_projects(self, users, categories, tags):
        """Create projects with various statuses"""
        now = timezone.now()
        
        projects_data = [
            {
                'title': 'AI-Powered Healthcare Diagnostic System',
                'details': 'Developing an AI system to help diagnose diseases early using machine learning and medical imaging. This project aims to make advanced diagnostics accessible to everyone.',
                'total_target': Decimal('50000.00'),
                'creator_idx': 0,
                'category_idx': 0,
                'tag_indices': [0, 6, 3],
                'start_time': now - timedelta(days=30),
                'end_time': now + timedelta(days=30),
                'is_featured': True,
                'status': 'running',
                'donated_amount': Decimal('35000.00'),
            },
            {
                'title': 'Sustainable Community Gardens Initiative',
                'details': 'Creating urban gardens to promote food security, environment awareness, and community bonding. We need funds to build 10 garden plots in underserved neighborhoods.',
                'total_target': Decimal('25000.00'),
                'creator_idx': 3,
                'category_idx': 4,
                'tag_indices': [1, 2, 8],
                'start_time': now - timedelta(days=15),
                'end_time': now + timedelta(days=45),
                'is_featured': True,
                'status': 'running',
                'donated_amount': Decimal('18000.00'),
            },
            {
                'title': 'Mental Health Support Platform',
                'details': 'Building a digital platform connecting people with trained mental health counselors. Our goal is to provide affordable mental health support to those in need.',
                'total_target': Decimal('40000.00'),
                'creator_idx': 1,
                'category_idx': 2,
                'tag_indices': [10, 11, 4],
                'start_time': now - timedelta(days=60),
                'end_time': now - timedelta(days=10),
                'is_featured': False,
                'status': 'completed',
                'donated_amount': Decimal('42500.00'),
            },
            {
                'title': 'Women in Tech Scholarship Program',
                'details': 'Launching a comprehensive scholarship and mentorship program for women entering tech careers. Supporting diversity in technology.',
                'total_target': Decimal('35000.00'),
                'creator_idx': 6,
                'category_idx': 1,
                'tag_indices': [11, 3, 2],
                'start_time': now - timedelta(days=5),
                'end_time': now + timedelta(days=60),
                'is_featured': True,
                'status': 'running',
                'donated_amount': Decimal('22000.00'),
            },
            {
                'title': 'Local Art Gallery Renovation',
                'details': 'Renovating our community\'s historic art gallery to showcase local talent and make art accessible to everyone. This space will serve as a cultural hub.',
                'total_target': Decimal('30000.00'),
                'creator_idx': 2,
                'category_idx': 3,
                'tag_indices': [0, 2, 5],
                'start_time': now + timedelta(days=10),
                'end_time': now + timedelta(days=90),
                'is_featured': False,
                'status': 'pending',
                'donated_amount': Decimal('5000.00'),
            },
            {
                'title': 'Clean Water Access for Rural Areas',
                'details': 'Installing water purification systems and wells in remote villages. Bringing safe drinking water to 500+ families.',
                'total_target': Decimal('60000.00'),
                'creator_idx': 4,
                'category_idx': 5,
                'tag_indices': [1, 2, 9],
                'start_time': now - timedelta(days=20),
                'end_time': now + timedelta(days=40),
                'is_featured': True,
                'status': 'running',
                'donated_amount': Decimal('45000.00'),
            },
            {
                'title': 'Youth Coding Bootcamp',
                'details': 'Free intensive coding bootcamp for underprivileged youth. Teaching in-demand tech skills to create job opportunities.',
                'total_target': Decimal('20000.00'),
                'creator_idx': 0,
                'category_idx': 1,
                'tag_indices': [3, 13, 14],
                'start_time': now - timedelta(days=45),
                'end_time': now - timedelta(days=5),
                'is_featured': False,
                'status': 'completed',
                'donated_amount': Decimal('21000.00'),
            },
            {
                'title': 'Micro-Enterprise Loan Program',
                'details': 'Providing small loans and business training to help entrepreneurs start their own businesses in underservice communities.',
                'total_target': Decimal('80000.00'),
                'creator_idx': 5,
                'category_idx': 6,
                'tag_indices': [8, 15, 2],
                'start_time': now - timedelta(days=10),
                'end_time': now + timedelta(days=50),
                'is_featured': True,
                'status': 'running',
                'donated_amount': Decimal('55000.00'),
            },
            {
                'title': 'Mobile Medical Clinic for Remote Areas',
                'details': 'Operating a mobile clinic to provide basic healthcare services, vaccinations, and health education in remote villages.',
                'total_target': Decimal('45000.00'),
                'creator_idx': 1,
                'category_idx': 2,
                'tag_indices': [2, 5, 10],
                'start_time': now + timedelta(days=5),
                'end_time': now + timedelta(days=75),
                'is_featured': False,
                'status': 'pending',
                'donated_amount': Decimal('8000.00'),
            },
            {
                'title': 'Open Source Educational Platform',
                'details': 'Creating a free, open-source online learning platform for students worldwide. Building community-driven content and features.',
                'total_target': Decimal('37500.00'),
                'creator_idx': 7,
                'category_idx': 0,
                'tag_indices': [14, 0, 3],
                'start_time': now - timedelta(days=25),
                'end_time': now + timedelta(days=35),
                'is_featured': True,
                'status': 'running',
                'donated_amount': Decimal('28000.00'),
            },
        ]
        
        projects = []
        for proj_data in projects_data:
            creator = users[proj_data.pop('creator_idx')]
            category = categories[proj_data.pop('category_idx')]
            tag_indices = proj_data.pop('tag_indices', [])
            
            project, created = Project.objects.get_or_create(
                title=proj_data['title'],
                created_by=creator,
                defaults={
                    **proj_data,
                    'category': category,
                }
            )
            
            if created:
                # Add tags
                for tag_idx in tag_indices:
                    if tag_idx < len(tags):
                        project.tags.add(tags[tag_idx])
                
                # Create multiple high-quality images for each project (2-4 images)
                num_images = random.randint(2, 4)
                try:
                    image_files = self.get_project_images(
                        project.title,
                        project.details,
                        count=num_images
                    )
                    
                    if image_files:
                        for image_file in image_files:
                            ProjectImage.objects.create(
                                project=project,
                                image=image_file
                            )
                        self.stdout.write(f'    ✓ Added {len(image_files)} images')
                    else:
                        self.stdout.write(self.style.WARNING(f'  ⚠ Could not create images for {project.title}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  ⚠ Error creating images for {project.title}: {str(e)}'))
                
                # Calculate average rating
                project.update_average_rating()
                
                self.stdout.write(f'  ✓ Created project: {project.title}')
            
            projects.append(project)
        
        return projects

    def get_random_profile_picture(self):
        """Download a random profile picture from an online service"""
        # Use Unsplash API for random user avatars (or Face API)
        # Fallback to DiceBear avatars which are reliable and don't require API keys
        names = ['Ahmed', 'Fatima', 'Mahmoud', 'Layla', 'Sara', 'Karim', 'Amira', 'Hassan']
        random_name = random.choice(names)
        
        # Using DiceBear API for consistent avatar generation
        avatar_url = f"https://api.dicebear.com/7.x/avataaars/png?seed={random_name}{random.randint(1, 1000)}&scale=80"
        
        try:
            response = requests.get(avatar_url, timeout=5)
            if response.status_code == 200:
                filename = f"profile_pics/{random_name}_{random.randint(1, 9999)}.png"
                return ContentFile(response.content, name=filename)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'  ⚠ Could not fetch profile picture from URL: {str(e)}'))
        
        return None

    def get_project_images(self, project_title: str, project_details: str, count: int = 3):
        """Fetch multiple high-quality images for a project using Picsum.photos"""
        import time
        images = []
        title_hash = hash(project_title) % 1000
        
        for idx in range(count):
            retries = 3
            success = False
            
            for attempt in range(retries):
                try:
                    # Use different endpoints to avoid rate limiting
                    seed_value = title_hash + idx * 100 + attempt * 10
                    image_url = f'https://picsum.photos/800/600?random={attempt + 1}&seed={seed_value}'
                    
                    response = requests.get(image_url, timeout=15, allow_redirects=True)
                    response.raise_for_status()
                    
                    if response.status_code == 200 and len(response.content) > 5000:
                        filename = f"projects/{project_title.replace(' ', '_')[:35]}_{idx+1}.jpg"
                        images.append(ContentFile(response.content, name=filename))
                        success = True
                        break
                    
                    time.sleep(0.5)  # Small delay between requests
                    
                except Exception as e:
                    if attempt < retries - 1:
                        time.sleep(1)  # Wait before retry
                    else:
                        self.stdout.write(self.style.WARNING(f'    ⚠ Image {idx+1}: Failed after {retries} attempts'))
        
        return images if images else None

    def generate_placeholder_image(self, title: str):
        """Generate a placeholder image for a project as fallback"""
        # Create image
        width, height = 400, 300
        colors = [
            (52, 152, 219),   # Blue
            (46, 204, 113),   # Green
            (155, 89, 182),   # Purple
            (230, 126, 34),   # Orange
            (231, 76, 60),    # Red
            (26, 188, 156),   # Teal
        ]
        bg_color = random.choice(colors)
        img = PILImage.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Add text
        text = title[:30]  # Limit text length
        text_position = (width // 2, height // 2)
        text_fill = (255, 255, 255)
        
        try:
            draw.text(
                text_position,
                text,
                fill=text_fill,
                anchor='mm'
            )
        except Exception:
            # If font fails, just continue without text
            pass
        
        # Save to file
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        
        filename = f"projects/{title.replace(' ', '_')[:30]}.jpg"
        return ContentFile(img_io.getvalue(), name=filename)

    def create_donations(self, users, projects):
        """Create realistic donations across projects"""
        donation_amounts = [Decimal(amt) for amt in ['100.00', '250.00', '500.00', '1000.00', '2500.00', '5000.00']]
        donation_count = 0
        
        for project in projects:
            if project.status != 'pending':
                # Randomly select 3-8 donors per project
                num_donors = random.randint(3, 8)
                selected_users = random.sample(users, min(num_donors, len(users)))
                
                for user in selected_users:
                    # Check if donation already exists
                    if not Donation.objects.filter(user=user, project=project).exists():
                        amount = random.choice(donation_amounts)
                        Donation.objects.create(
                            user=user,
                            project=project,
                            amount=amount,
                            created_at=project.start_time + timedelta(days=random.randint(1, 20))
                        )
                        donation_count += 1
        
        self.stdout.write(f'  ✓ Created {donation_count} donations')

    def create_ratings(self, users, projects):
        """Create ratings for projects"""
        rating_count = 0
        
        for project in projects:
            if project.status in ['running', 'completed']:
                # Get donors for this project
                donors = list(project.donations.values_list('user_id', flat=True).distinct())
                
                for user_id in donors:
                    user = User.objects.get(id=user_id)
                    # Check if rating already exists
                    if not Rating.objects.filter(user=user, project=project).exists():
                        score = random.randint(3, 5)  # 3-5 stars (positive ratings)
                        Rating.objects.create(
                            user=user,
                            project=project,
                            score=score,
                        )
                        rating_count += 1
        
        # Update project average ratings
        for project in projects:
            project.update_average_rating()
        
        self.stdout.write(f'  ✓ Created {rating_count} ratings')

    def create_comments(self, users, projects):
        """Create comments and replies on projects"""
        comment_texts = [
            'Great project! Really looking forward to seeing this succeed.',
            'This is exactly what our community needs. Fully supporting this.',
            'Impressive team and clear vision. Definitely backing this.',
            'The impact potential here is huge. Love the approach.',
            'Transparency and accountability are key. Well done on that front.',
            'This will make a real difference. Count me in!',
            'Such an important initiative. Better world starts here.',
            'Professional execution and genuine impact. Respect.',
            'Game-changer for sure. Excited to be part of this journey.',
            'The team\'s passion is evident. This will succeed.',
            'Amazing to see people working for positive change.',
            'Clear roadmap and realistic goals. Very impressive.',
        ]
        
        reply_texts = [
            'Completely agree! This is what makes the difference.',
            'You nailed it. That\'s exactly why I believe in this project.',
            'Could not agree more. The impact will be substantial.',
            'Well said. So important for our community.',
            'You captured the essence perfectly.',
            'Thanks for the support! Your backing means a lot.',
        ]
        
        comment_count = 0
        
        for project in projects:
            if project.status != 'pending':
                # Create 3-6 main comments per project
                num_comments = random.randint(3, 6)
                selected_users = random.sample(users, min(num_comments, len(users)))
                
                for user in selected_users:
                    # Check if comment exists (avoid multiple comments per user per project)
                    comment_exists = Comment.objects.filter(
                        user=user,
                        project=project,
                        parent=None
                    ).exists()
                    
                    if not comment_exists:
                        comment = Comment.objects.create(
                            user=user,
                            project=project,
                            text=random.choice(comment_texts),
                            parent=None,
                        )
                        comment_count += 1
                        
                        # Sometimes add replies to comments
                        if random.choice([True, False]):
                            reply_user = random.choice([u for u in users if u != user])
                            reply_comment_exists = Comment.objects.filter(
                                user=reply_user,
                                project=project,
                                parent=comment
                            ).exists()
                            
                            if not reply_comment_exists:
                                reply_comment = Comment.objects.create(
                                    user=reply_user,
                                    project=project,
                                    parent=comment,
                                    text=random.choice(reply_texts),
                                )
                                comment_count += 1
        
        self.stdout.write(f'  ✓ Created {comment_count} comments and replies')
