from django.contrib import admin

from .models import Project, Asset


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status', 'user', 'created_at')
    list_filter = ('type', 'status', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'file_type', 'file_size', 'user', 'created_at')
    list_filter = ('file_type', 'created_at')
    search_fields = ('name', 'filename')
    readonly_fields = ('created_at',)
