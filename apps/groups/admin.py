from django.contrib import admin
from .models import StudyGroup, GroupMembership


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'is_private', 'created_at')
    search_fields = ('name', 'creator__email')
    list_filter = ('is_private',)


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'joined_at')
    search_fields = ('user__email', 'group__name')
