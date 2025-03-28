from django.contrib import admin
from .models import StudyGroup, GroupMembership, SharedFile


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'is_private', 'created_at')
    search_fields = ('name', 'creator__email')
    list_filter = ('is_private',)


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'joined_at')
    search_fields = ('user__email', 'group__name')

@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'group', 'uploaded_by', 'uploaded_at')
    list_filter = ('group',)
    search_fields = ('file', 'uploaded_by__email')
    readonly_fields = ('uploaded_at',)