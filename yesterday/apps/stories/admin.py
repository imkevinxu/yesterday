from django.contrib import admin

from .models import Story


class StoryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'story', 'created')
    search_fields = ('uuid', 'story')

admin.site.register(Story, StoryAdmin)
