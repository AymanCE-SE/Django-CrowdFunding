# # from django.test import TestCase

# # Create your tests here.
# <!-- The updated project_detail.html template -->
# {% extends 'base.html' %}
# {% load static %}
# {% load project_extras %}

# {% block content %}
# <div class="container py-4">
#     <div class="row g-4">
#         <!-- Main Content -->
#         <div class="col-lg-8">
#             <div class="card shadow-sm mb-4">
#                 <div class="card-body">
#                     <div class="d-flex justify-content-between align-items-start mb-3">
#                         <div>
#                             <h1 class="h2 mb-2">{{ project.title }}</h1>
#                             <p class="text-muted mb-0">
#                                 <i class="fas fa-calendar-alt me-2"></i>Created {{ project.created_at|date }}
#                             </p>
#                         </div>
#                         <div class="d-flex align-items-center">
#                             {% if user.is_authenticated and not is_owner %}
#                             <button class="btn btn-sm btn-outline-danger me-2" data-bs-toggle="modal" data-bs-target="#reportProjectModal">
#                                 <i class="fas fa-flag me-1"></i> Report
#                             </button>
#                             {% endif %}
                            
#                             {% if is_owner %}
#                             <div class="dropdown">
#                                 <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
#                                     <i class="fas fa-cog"></i>
#                                 </button>
#                                 <ul class="dropdown-menu dropdown-menu-end">
#                                     <li>
#                                         <a class="dropdown-item text-primary" href="{% url 'projects:edit_project' pk=project.pk %}">
#                                             <i class="fas fa-edit me-2"></i>Edit Project
#                                         </a>
#                                     </li>
#                                     {% if project.can_be_deleted %}
#                                     <li>
#                                         <a class="dropdown-item text-danger" href="{% url 'projects:delete_project' pk=project.pk %}">
#                                             <i class="fas fa-trash me-2"></i>Delete Project
#                                         </a>
#                                     </li>
#                                     {% endif %}
#                                 </ul>
#                             </div>
#                             {% endif %}
#                         </div>
#                     </div>

#                     {% if project.images.exists %}
#                     <div id="projectCarousel" class="carousel slide mb-4" data-bs-ride="carousel">
#                         <div class="carousel-inner rounded">
#                             {% for image in project.images.all %}
#                             <div class="carousel-item {% if forloop.first %}active{% endif %}">
#                                 <img src="{{ image.image.url }}" class="d-block w-100 project-img" alt="Project Image">
#                             </div>
#                             {% endfor %}
#                         </div>
#                         {% if project.images.count > 1 %}
#                         <button class="carousel-control-prev" type="button" data-bs-target="#projectCarousel" data-bs-slide="prev">
#                             <span class="carousel-control-prev-icon"></span>
#                         </button>
#                         <button class="carousel-control-next" type="button" data-bs-target="#projectCarousel" data-bs-slide="next">
#                             <span class="carousel-control-next-icon"></span>
#                         </button>
#                         <div class="carousel-indicators">
#                             {% for image in project.images.all %}
#                             <button type="button" data-bs-target="#projectCarousel" data-bs-slide-to="{{ forloop.counter0 }}"
#                                     class="{% if forloop.first %}active{% endif %}"></button>
#                             {% endfor %}
#                         </div>
#                         {% endif %}
#                     </div>
#                     {% endif %}

#                     <!-- Tabs Navigation -->
#                     <ul class="nav nav-tabs nav-fill mb-3" role="tablist">
#                         <li class="nav-item" role="presentation">
#                             <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#description">
#                                 <i class="fas fa-info-circle me-2"></i>Description
#                             </button>
#                         </li>
#                         <li class="nav-item" role="presentation">
#                             <button class="nav-link" data-bs-toggle="tab" data-bs-target="#comments">
#                                 <i class="fas fa-comments me-2"></i>Comments
#                                 <span class="badge bg-secondary ms-1">{{ comments.count }}</span>
#                             </button>
#                         </li>
#                         <li class="nav-item" role="presentation">
#                             <button class="nav-link" data-bs-toggle="tab" data-bs-target="#updates">
#                                 <i class="fas fa-bell me-2"></i>Updates
#                             </button>
#                         </li>
#                     </ul>

#                     <!-- Tabs Content -->
#                     <div class="tab-content">
#                         <!-- Description Tab -->
#                         <div class="tab-pane fade show active" id="description">
#                             <div class="p-3">
#                                 {{ project.details|linebreaks }}
#                                 {% if project.tags.all %}
#                                 <div class="mt-4">
#                                     {% for tag in project.tags.all %}
#                                     <span class="badge bg-light text-dark me-2">#{{ tag.name }}</span>
#                                     {% endfor %}
#                                 </div>
#                                 {% endif %}
#                             </div>
#                         </div>

#                         <!-- Comments Tab -->
#                         <div class="tab-pane fade" id="comments">
#                             <div class="p-3">
#                                 {% if user.is_authenticated %}
#                                 <form id="comment-form" method="post" action="{% url 'projects:add_comment' pk=project.pk %}" class="mb-4" data-ajax-comment="true">
#                                     {% csrf_token %}
#                                     <div class="form-group">
#                                         {{ comment_form.text }}
#                                     </div>
#                                     <button type="submit" class="btn btn-primary mt-2">
#                                         <i class="fas fa-paper-plane me-2"></i>Add Comment
#                                     </button>
#                                 </form>
#                                 {% endif %}
                                
#                                 <div id="comments-container" class="comments-list">
#                                     <!-- Root comments -->
#                                     {% for comment in comments %}
#                                     {% if not comment.parent %}
#                                     <div class="comment-thread mb-4">
#                                         <div class="comment-container" id="comment-{{ comment.id }}">
#                                             <div class="card border-0 shadow-sm mb-2">
#                                                 <div class="card-body">
#                                                     <div class="d-flex justify-content-between align-items-center mb-2">
#                                                         <div class="d-flex align-items-center">
#                                                             <img src="{% static 'images/profile.png' %}" 
#                                                                 class="rounded-circle me-2" 
#                                                                 width="32" height="32" 
#                                                                 alt="{{ comment.user.username }}">
#                                                             <h6 class="card-subtitle mb-0">{{ comment.user.username }}</h6>
#                                                         </div>
#                                                         <div class="d-flex">
#                                                             <small class="text-muted me-2">{{ comment.created_at|timesince }} ago</small>
#                                                             {% if user.is_authenticated and user != comment.user %}
#                                                             <button type="button" class="btn btn-link btn-sm text-danger report-btn p-0" 
#                                                                     data-bs-toggle="modal" 
#                                                                     data-bs-target="#reportCommentModal"
#                                                                     data-comment-id="{{ comment.id }}">
#                                                                 <i class="fas fa-flag"></i>
#                                                             </button>
#                                                             {% endif %}
#                                                         </div>
#                                                     </div>
#                                                     <p class="card-text mb-1">{{ comment.text }}</p>
#                                                     <!-- Reply Button -->
#                                                     {% if user.is_authenticated %}
#                                                     <button class="btn btn-link btn-sm text-primary reply-btn p-0" data-comment-id="{{ comment.id }}">
#                                                         <i class="fas fa-reply me-1"></i>Reply
#                                                     </button>
#                                                     {% endif %}
#                                                     <!-- Reply Form (hidden by default) -->
#                                                     <div class="reply-form-container" id="reply-form-{{ comment.id }}" style="display:none;">
#                                                         <form method="post" action="{% url 'projects:add_comment' pk=project.pk %}" data-ajax-reply="true">
#                                                             {% csrf_token %}
#                                                             <input type="hidden" name="parent" value="{{ comment.id }}">
#                                                             <div class="form-group mt-2">
#                                                                 <textarea name="text" class="form-control reply-text" rows="2" placeholder="Write your reply..."></textarea>
#                                                             </div>
#                                                             <div class="mt-2">
#                                                                 <button type="submit" class="btn btn-sm btn-primary">Submit Reply</button>
#                                                                 <button type="button" class="btn btn-sm btn-light cancel-reply">Cancel</button>
#                                                             </div>
#                                                         </form>
#                                                     </div>
#                                                 </div>
#                                             </div>
                                            
#                                             <!-- Replies to this comment -->
#                                             <div class="replies-container ms-4">
#                                                 {% for reply in comment.replies.all %}
#                                                 <div class="card border-0 shadow-sm mb-2" id="comment-{{ reply.id }}">
#                                                     <div class="card-body">
#                                                         <div class="d-flex justify-content-between align-items-center mb-2">
#                                                             <div class="d-flex align-items-center">
#                                                                 <img src="{% static 'images/profile.png' %}" 
#                                                                     class="rounded-circle me-2" 
#                                                                     width="28" height="28" 
#                                                                     alt="{{ reply.user.username }}">
#                                                                 <div>
#                                                                     <h6 class="card-subtitle mb-0">{{ reply.user.username }}</h6>
#                                                                     <small class="text-muted">Replying to {{ reply.parent.user.username }}</small>
#                                                                 </div>
#                                                             </div>
#                                                             <div class="d-flex">
#                                                                 <small class="text-muted me-2">{{ reply.created_at|timesince }} ago</small>
#                                                                 {% if user.is_authenticated and user != reply.user %}
#                                                                 <button type="button" class="btn btn-link btn-sm text-danger report-btn p-0" 
#                                                                         data-bs-toggle="modal" 
#                                                                         data-bs-target="#reportCommentModal"
#                                                                         data-comment-id="{{ reply.id }}">
#                                                                     <i class="fas fa-flag"></i>
#                                                                 </button>
#                                                                 {% endif %}
#                                                             </div>
#                                                         </div>
#                                                         <p class="card-text mb-1">{{ reply.text }}</p>
#                                                         <!-- Reply Button -->
#                                                         {% if user.is_authenticated %}
#                                                         <button class="btn btn-link btn-sm text-primary reply-btn p-0" data-comment-id="{{ comment.id }}">
#                                                             <i class="fas fa-reply me-1"></i>Reply
#                                                         </button>
#                                                         {% endif %}
#                                                     </div>
#                                                 </div>
#                                                 {% endfor %}
#                                             </div>
#                                         </div>
#                                     </div>
#                                     {% endif %}
#                                     {% empty %}
#                                     <div class="text-center text-muted py-4">
#                                         <i class="fas fa-comments fa-2x mb-3"></i>
#                                         <p>No comments yet. Be the first to comment!</p>
#                                     </div>
#                                     {% endfor %}
#                                 </div>
#                             </div>
#                         </div>

#                         <!-- Updates Tab -->
#                         <div class="tab-pane fade" id="updates">
#                             <div class="p-3">
#                                 <div class="text-center text-muted py-4">
#                                     <i class="fas fa-bell fa-2x mb-3"></i>
#                                     <p>Project updates will appear here.</p>
#                                 </div>
#                             </div>
#                         </div>
#                     </div>
#                 </div>
#             </div>
#         </div>

#         <!-- Sidebar Content -->
#         <div class="col-lg-4">
#             <!-- Project Status -->
#             <div class="card shadow-sm mb-4">
#                 <div class="card-body">
#                     <h2 class="card-title h4 mb-3">{{ project.title }}</h2>
#                     <div class="progress mb-3" style="height: 12px;">
#                         <div class="progress-bar bg-success" role="progressbar" 
#                              style="width: {{ project.progress }}%"
#                              aria-valuenow="{{ project.progress }}" 
#                              aria-valuemin="0" aria-valuemax="100">
#                         </div>
#                     </div>
                    
#                     <div class="d-flex justify-content-between mb-4">
#                         <div class="text-center">
#                             <h6 class="mb-1">Raised</h6>
#                             <h4 class="text-success mb-0">{{ total_donations }} EGP</h4>
#                         </div>
#                         <div class="text-center">
#                             <h6 class="mb-1">Target</h6>
#                             <h4 class="mb-0">{{ project.total_target }} EGP</h4>
#                         </div>
#                     </div>

#                     <div class="mb-4">
#                         <div class="d-flex justify-content-between align-items-center mb-2">
#                             <span><i class="fas fa-clock me-2"></i>Time Remaining</span>
#                             <strong>{{ project.time_remaining }}</strong>
#                         </div>
#                         <div class="d-flex justify-content-between align-items-center mb-2">
#                             <span><i class="fas fa-users me-2"></i>Backers</span>
#                             <strong>{{ project.get_donation_stats.total_donors }}</strong>
#                         </div>
#                         <div class="d-flex justify-content-between align-items-center">
#                             <span><i class="fas fa-star me-2"></i>Rating</span>
#                             <strong id="average-rating">{{ average_rating|default:"No ratings" }}</strong>
#                         </div>
#                     </div>
                    
#                     {% if user.is_authenticated %}
#                         {% with status=project.get_status %}
#                             <div class="mb-4">
#                                 {% if status == 'coming_soon' %}
#                                     <div class="alert alert-info">
#                                         <i class="fas fa-clock me-2"></i>{{ project.get_status_message }}
#                                     </div>
#                                     <button class="btn btn-secondary btn-lg w-100" disabled>
#                                         <i class="fas fa-clock me-2"></i>Coming Soon
#                                     </button>
#                                 {% elif status == 'ended' %}
#                                     <div class="alert alert-warning">
#                                         <i class="fas fa-exclamation-circle me-2"></i>{{ project.get_status_message }}
#                                     </div>
#                                     <button class="btn btn-secondary btn-lg w-100" disabled>
#                                         <i class="fas fa-times-circle me-2"></i>Project Ended
#                                     </button>
#                                 {% elif status == 'funded' %}
#                                     <div class="alert alert-success">
#                                         <i class="fas fa-check-circle me-2"></i>{{ project.get_status_message }}
#                                     </div>
#                                     <button class="btn btn-success btn-lg w-100" disabled>
#                                         <i class="fas fa-check-circle me-2"></i>Fully Funded
#                                     </button>
#                                 {% else %}
#                                     <div class="alert alert-info">
#                                         <i class="fas fa-info-circle me-2"></i>
#                                         <strong>Target:</strong> {{ project.total_target|floatformat:2 }} EGP<br>
#                                         <strong>Still Needed:</strong> {{ project.get_status_message }}
#                                     </div>
#                                     <a href="{% url 'projects:donate_to_project' pk=project.pk %}" 
#                                        class="btn btn-success btn-lg w-100">
#                                         <i class="fas fa-hand-holding-usd me-2"></i>Donate Now
#                                     </a>
#                                 {% endif %}
#                             </div>
#                         {% endwith %}
#                     {% else %}
#                         <div class="alert alert-info">
#                             <i class="fas fa-info-circle me-2"></i>Please login to donate
#                         </div>
#                         <a href="{% url 'login' %}?next={{ request.path }}" 
#                            class="btn btn-primary btn-lg w-100">
#                             <i class="fas fa-sign-in-alt me-2"></i>Login to Donate
#                         </a>
#                     {% endif %}
                    
#                     <!-- Interactive Rating Widget -->
#                     {% if user.is_authenticated and not is_owner %}
#                     <div id="rating-widget" data-current-rating="{{ user_rating|default:0 }}" data-project-id="{{ project.pk }}">
#                         <div class="star-rating mb-2">
#                             {% for star in "12345"|make_list %}
#                                 <i class="rating-star {% if user_rating|default:0 >= forloop.counter %}fas{% else %}far{% endif %} fa-star" data-score="{{ forloop.counter }}"></i>
#                             {% endfor %}
#                         </div>
#                         <form id="rating-form" method="post" action="{% url 'projects:rate_project' pk=project.pk %}">
#                             {% csrf_token %}
#                             <input type="hidden" name="score" id="rating-score" value="{{ user_rating|default:0 }}">
#                             <button type="submit" class="btn btn-primary btn-sm" id="submit-rating">Submit Rating</button>
#                         </form>
#                     </div>
#                     {% elif user_rating %}
#                         <div>
#                             <span>Your rating: {{ user_rating }}</span>
#                         </div>
#                     {% endif %}
                    
#                 </div>
#             </div>

#             <!-- Creator Info -->
#             <div class="card shadow-sm mb-4">
#                 <div class="card-body">
#                     <h5 class="card-title">Project Creator</h5>
#                     <div class="d-flex align-items-center mb-3">
#                         <img src="{% static 'images/profile.png' %}" 
#                              class="rounded-circle me-3" 
#                              width="50" height="50" 
#                              alt="{{ project.created_by.username }}">
#                         <div>
#                             <h6 class="mb-0">{{ project.created_by.username }}</h6>
#                             <small class="text-muted">Member since {{ project.created_by.date_joined|date }}</small>
#                         </div>
#                     </div>
#                 </div>
#             </div>

#             <!-- Top Donors -->
#             <div class="card shadow-sm">
#                 <div class="card-body">
#                     <h5 class="card-title">Top Supporters</h5>
#                     {% for donor in project.get_top_donors %}
#                     <div class="d-flex justify-content-between align-items-center mb-2">
#                         <span>{{ donor.user__username }}</span>
#                         <strong>{{ donor.total_amount }} EGP</strong>
#                     </div>
#                     {% empty %}
#                     <p class="text-muted">No donations yet.</p>
#                     {% endfor %}
#                 </div>
#             </div>
#         </div>
#     </div>
# </div>

# <!-- Report Comment Modal -->
# <div class="modal fade" id="reportCommentModal" tabindex="-1" aria-labelledby="reportCommentModalLabel" aria-hidden="true">
#     <div class="modal-dialog">
#         <div class="modal-content">
#             <div class="modal-header">
#                 <h5 class="modal-title" id="reportCommentModalLabel">Report Comment</h5>
#                 <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
#             </div>
#             <div class="modal-body">
#                 <form id="reportCommentForm">
#                     {% csrf_token %}
#                     <input type="hidden" name="content_type" value="comment">
#                     <input type="hidden" name="content_id" id="reportedCommentId">
                    
#                     <div class="mb-3">
#                         <label for="commentReportReason" class="form-label">Reason for reporting</label>
#                         <select class="form-select" id="commentReportReason" name="reason" required>
#                             <option value="">Select a reason</option>
#                             <option value="spam">Spam or misleading</option>
#                             <option value="inappropriate">Inappropriate content</option>
#                             <option value="copyright">Copyright violation</option>
#                             <option value="fraud">Fraud or scam</option>
#                             <option value="other">Other reason</option>
#                         </select>
#                     </div>
#                     <div class="mb-3">
#                         <label for="commentReportDetails" class="form-label">Additional details</label>
#                         <textarea class="form-control" id="commentReportDetails" name="details" rows="3" placeholder="Please provide additional details about your report"></textarea>
#                     </div>
#                 </form>
#             </div>
#             <div class="modal-footer">
#                 <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
#                 <button type="button" class="btn btn-danger" id="submitCommentReport">Submit Report</button>
#             </div>
#         </div>
#     </div>
# </div>

# <!-- Report Project Modal -->
# <div class="modal fade" id="reportProjectModal" tabindex="-1" aria-labelledby="reportProjectModalLabel" aria-hidden="true">
#     <div class="modal-dialog">
#         <div class="modal-content">
#             <div class="modal-header">
#                 <h5 class="modal-title" id="reportProjectModalLabel">Report Project</h5>
#                 <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
#             </div>
#             <div class="modal-body">
#                 <form id="reportProjectForm">
#                     {% csrf_token %}
#                     <input type="hidden" name="content_type" value="project">
#                     <input type="hidden" name="content_id" value="{{ project.pk }}">
                    
#                     <div class="mb-3">
#                         <label for="projectReportReason" class="form-label">Reason for reporting</label>
#                         <select class="form-select" id="projectReportReason" name="reason" required>
#                             <option value="">Select a reason</option>
#                             <option value="spam">Spam or misleading</option>
#                             <option value="inappropriate">Inappropriate content</option>
#                             <option value="copyright">Copyright violation</option>
#                             <option value="fraud">Fraud or scam</option>
#                             <option value="other">Other reason</option>
#                         </select>
#                     </div>
#                     <div class="mb-3">
#                         <label for="projectReportDetails" class="form-label">Additional details</label>
#                         <textarea class="form-control" id="projectReportDetails" name="details" rows="3" placeholder="Please provide additional details about your report"></textarea>
#                     </div>
#                 </form>
#             </div>
#             <div class="modal-footer">
#                 <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
#                 <button type="button" class="btn btn-danger" id="submitProjectReport">Submit Report</button>
#             </div>
#         </div>
#     </div>
# </div>
# {% endblock %}

# {% block extra_css %}
# <style>
# /* Carousel Styles */
# .carousel {
#     border-radius: 8px;
#     overflow: hidden;
# }
# .project-img {
#     height: 400px;
#     object-fit: cover;
# }

# /* Progress Bar */
# .progress {
#     height: 12px;
#     border-radius: 10px;
#     background-color: #e9ecef;
# }
# .progress-bar {
#     transition: width 0.6s ease;
# }

# /* Comments Section */
# .comment-thread {
#     margin-left: 2rem;
# }
# .replies-container {
#     margin-left: 2.5rem;
# }
# .reply-form-container {
#     margin-top: 1rem;
#     padding: 1rem;
#     background-color: #f8f9fa;
#     border-radius: 8px;
# }

# /* Rating Stars */
# .star-rating {
#     display: inline-flex;
#     gap: 4px;
# }
# .rating-star {
#     cursor: pointer;
#     font-size: 1.25rem;
#     color: #dee2e6;
#     transition: color 0.2s;
# }
# .rating-star.active,
# .rating-star:hover {
#     color: #ffc107;
# }
# .star-rating:hover .rating-star {
#     color: #dee2e6;
# }
# .star-rating:hover .rating-star:hover,
# .star-rating:hover .rating-star:hover ~ .rating-star {
#     color: #ffc107;
# }

# /* Cards and General Styling */
# .card {
#     border: none;
#     box-shadow: 0 2px 4px rgba(0,0,0,0.05);
#     transition: transform 0.2s;
# }
# .card:hover {
#     transform: translateY(-2px);
# }
# .btn-link {
#     text-decoration: none;
# }
# .btn-link:hover {
#     text-decoration: underline;
# }

# /* Tags */
# .badge {
#     transition: all 0.2s;
# }
# .badge:hover {
#     transform: translateY(-1px);
# }

# /* Report Buttons */
# .report-btn {
#     opacity: 0.5;
#     transition: opacity 0.2s;
# }
# .report-btn:hover {
#     opacity: 1;
# }
# </style>
# {% endblock %}

# {% block extra_js %}
# <script>
# document.addEventListener('DOMContentLoaded', function() {
#     // Rating System
#     const ratingWidget = document.getElementById('rating-widget');
#     if (ratingWidget) {
#         const ratingForm = document.getElementById('rating-form');
#         const ratingScore = document.getElementById('rating-score');
#         const ratingStars = document.querySelectorAll('.rating-star');
#         const averageRating = document.getElementById('average-rating');
        
#         // Update stars visually
#         function updateStars(score) {
#             ratingStars.forEach(star => {
#                 star.classList.toggle('active', parseInt(star.dataset.score) <= score);
#             });
#         }

#         // Handle star clicks with AJAX
#         ratingStars.forEach(star => {
#             star.addEventListener('click', function() {
#                 const score = this.dataset.score;
#                 ratingScore.value = score;
                
#                 fetch(ratingForm.action, {
#                     method: 'POST',
#                     body: new FormData(ratingForm),
#                     headers: {
#                         'X-Requested-With': 'XMLHttpRequest'
#                     }
#                 })
#                 .then(response => response.json())
#                 .then(data => {
#                     if (data.success) {
#                         updateStars(score);
#                         averageRating.textContent = data.average_rating;
#                     }
#                 })
#                 .catch(error => console.error('Error:', error));
#             });
#         });
#     }

#     // Comment System
#     const commentForm = document.getElementById('comment-form');
#     if (commentForm) {
#         commentForm.addEventListener('submit', function(e) {
#             e.preventDefault();
            
#             fetch(this.action, {
#                 method: 'POST',
#                 body: new FormData(this),
#                 headers: {
#                     'X-Requested-With': 'XMLHttpRequest'
#                 }
#             })
#             .then(response => response.json())
#             .then(data => {
#                 if (data.success) {
#                     location.reload(); // Refresh to show new comment
#                 }
#             })
#             .catch(error => console.error('Error:', error));
#         });
#     }

#     // Reply System
#     document.querySelectorAll('.reply-btn').forEach(button => {
#         button.addEventListener('click', function() {
#             const commentId = this.dataset.commentId;
#             const replyForm = document.getElementById(`reply-form-${commentId}`);
#             replyForm.style.display = replyForm.style.display === 'none' ? 'block' : 'none';
#         });
#     });

#     document.querySelectorAll('.cancel-reply').forEach(button => {
#         button.addEventListener('click', function() {
#             this.closest('.reply-form-container').style.display = 'none';
#         });
#     });

#     // Report System
#     const reportCommentModal = document.getElementById('reportCommentModal');
#     if (reportCommentModal) {
#         reportCommentModal.addEventListener('show.bs.modal', function(event) {
#             const button = event.relatedTarget;
#             const commentId = button.dataset.commentId;
#             document.getElementById('reportedCommentId').value = commentId;
#         });

#         document.getElementById('submitCommentReport').addEventListener('click', function() {
#             const form = document.getElementById('reportCommentForm');
#             fetch('/projects/report/', {
#                 method: 'POST',
#                 body: new FormData(form),
#                 headers: {
#                     'X-Requested-With': 'XMLHttpRequest'
#                 }
#             })
#             .then(response => response.json())
#             .then(data => {
#                 if (data.success) {
#                     bootstrap.Modal.getInstance(reportCommentModal).hide();
#                     alert('Report submitted successfully');
#                 }
#             })
#             .catch(error => console.error('Error:', error));
#         });
#     }

#     // Project Report System
#     const reportProjectModal = document.getElementById('reportProjectModal');
#     if (reportProjectModal) {
#         document.getElementById('submitProjectReport').addEventListener('click', function() {
#             const form = document.getElementById('reportProjectForm');
#             fetch('/projects/report/', {
#                 method: 'POST',
#                 body: new FormData(form),
#                 headers: {
#                     'X-Requested-With': 'XMLHttpRequest'
#                 }
#             })
#             .then(response => response.json())
#             .then(data => {
#                 if (data.success) {
#                     bootstrap.Modal.getInstance(reportProjectModal).hide();
#                     alert('Report submitted successfully');
#                 }
#             })
#             .catch(error => console.error('Error:', error));
#         });
#     }

#     // Carousel Navigation
#     const carousel = document.getElementById('projectCarousel');
#     if (carousel) {
#         const indicators = carousel.querySelectorAll('.carousel-indicators button');
#         indicators.forEach(indicator => {
#             indicator.addEventListener('click', function() {
#                 this.classList.add('active');
#             });
#         });
#     }
# });
# </script>
# {% endblock %}
