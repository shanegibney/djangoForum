from django.contrib import admin
from .models import FileModel
from .forms import FileForm

class FileModelAdmin(admin.ModelAdmin):
    form = FileForm
    fields = ('title', 'description', 'pub_date', 'submitted_date', 'author', 'user', 'approved', 'upload', 'vote')
    pass
admin.site.register(FileModel, FileModelAdmin)
