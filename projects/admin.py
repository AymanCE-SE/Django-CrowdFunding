from django.contrib import admin
from .models import Category, Project, ProjectImage, Tag, Donation, Comment, Rating, Report

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    max_num = 5

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_by', 'status', 'is_featured', 'created_at', 'get_tags']
    list_filter = ['status', 'is_featured', 'category', 'tags']
    search_fields = ['title', 'details', 'tags__name']
    date_hierarchy = 'created_at'
    actions = ['make_running', 'make_completed', 'make_cancelled']
    inlines = [ProjectImageInline]
    filter_horizontal = ('tags',)  # Add this for better tag selection interface
    
    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = "Tags"

    def make_running(self, request, queryset):
        queryset.update(status='running')
    make_running.short_description = "Mark selected projects as running"

    def make_completed(self, request, queryset):
        queryset.update(status='completed')
    make_completed.short_description = "Mark selected projects as completed"

    def make_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    make_cancelled.short_description = "Mark selected projects as cancelled"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'project__title')
    readonly_fields = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'text_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'project__title', 'text')
    readonly_fields = ('created_at',)

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comment'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('user__username', 'project__title')
    readonly_fields = ('created_at',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'report_type', 'project', 'comment', 'reason', 'created_at')
    list_filter = ('report_type', 'created_at')
    search_fields = ('reason', 'reporter__username')