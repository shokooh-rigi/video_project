from django.contrib import admin
from .models import Category, Video


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'uploaded_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Video, VideoAdmin)
