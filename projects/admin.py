from django.contrib import admin
from .models import Category, Project, ProjectImage, Tag, Donation, Comment, Rating

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    max_num = 5

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'category', 'total_target', 'donated_amount', 'progress', 'get_status')
    list_filter = ('category', 'created_at', 'start_time', 'end_time')
    search_fields = ('title', 'details', 'created_by__username')
    readonly_fields = ('created_at', 'donated_amount')
    filter_horizontal = ('tags',)
    inlines = [ProjectImageInline]
    
    def progress(self, obj):
        return f"{obj.progress}%"
    progress.short_description = 'Funding Progress'

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
