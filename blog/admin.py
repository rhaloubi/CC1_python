from django.contrib import admin
from .models import Category, Post, Comment

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'category', 'views')
    list_filter = ('date_posted', 'category')
    search_fields = ('title', 'content')
    date_hierarchy = 'date_posted'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'get_author', 'date_posted')
    list_filter = ('date_posted',)
    search_fields = ('content',)
    
    def get_author(self, obj):
        return obj.author.username if obj.author else obj.author_name
    get_author.short_description = 'Author'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
