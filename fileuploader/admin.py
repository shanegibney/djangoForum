from django.contrib import admin
from .models import FileModel
from .forms import FileForm

class FileModelAdmin(admin.ModelAdmin):
    form = FileForm
    fields = ('title', 'description', 'categories', 'pub_date', 'submitted_date', 'author', 'user', 'approved', 'upload', 'vote')
    # pass
    list_display = ['title', 'approved', 'author', 'user', 'categories', 'description', 'pub_date', 'submitted_date', 'upload', 'vote']
admin.site.register(FileModel, FileModelAdmin)
