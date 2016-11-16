from django.contrib import admin
from .models import TopicModel, PostModel, NewUserModel, BlogModel, InfoModel, TempModel
from .forms import BlogForm, TopicForm

class TopicModelAdmin(admin.ModelAdmin):
    form = TopicForm
    fields = ('topic', 'categories', 'author', 'topicAuthor', 'views')
    # pass
    list_display = ['topic', 'topicAuthor', 'author', 'categories', 'views']

admin.site.register(TopicModel, TopicModelAdmin)

class PostModelAdmin(admin.ModelAdmin):
    form = TopicForm
    fields = ('post', 'pub_date', 'user', 'topic', 'vote')
    # pass
    list_display = ['post', 'pub_date', 'user', 'topic', 'vote']

admin.site.register(PostModel, PostModelAdmin)

class InfoModelAdmin(admin.ModelAdmin):
    list_display = ['topicid', 'postid', 'author', 'post', 'date']

admin.site.register(InfoModel, InfoModelAdmin)

class NewUserModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'posts', 'files', 'articles']

admin.site.register(NewUserModel, NewUserModelAdmin)

class TempModelAdmin(admin.ModelAdmin):
    list_display = ['topicid', 'date', 'author']

admin.site.register(TempModel, TempModelAdmin)

class BlogModelAdmin(admin.ModelAdmin):
    form = BlogForm
    fields = ('title', 'article', 'pub_date', 'submitted_date', 'author', 'categories', 'approved')
    # pass
    list_display = ['title', 'approved', 'author', 'categories', 'pub_date', 'submitted_date']

admin.site.register(BlogModel, BlogModelAdmin)
