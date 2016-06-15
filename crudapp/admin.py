from django.contrib import admin
from .models import TopicModel, PostModel, BlogModel, InfoModel
from .forms import BlogForm

admin.site.register(TopicModel)
admin.site.register(PostModel)
admin.site.register(InfoModel)

class BlogModelAdmin(admin.ModelAdmin):
    form = BlogForm
    fields = ('title', 'article', 'pub_date', 'submitted_date', 'author', 'categories', 'approved')
    # pass
    list_display = ['title', 'approved', 'author', 'categories', 'pub_date', 'submitted_date']

admin.site.register(BlogModel, BlogModelAdmin)
