from django.contrib import admin
from .models import Topic, Post, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_banned')
    list_filter = ('is_banned',)
    search_fields = ('user__username',)


admin.site.register(Topic)
admin.site.register(Post)