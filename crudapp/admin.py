from django.contrib import admin
from .models import TopicModel, PostModel, BlogModel
# from .forms import NameForm

# Register your models here.
# admin.site.register(Members)
admin.site.register(TopicModel)
admin.site.register(PostModel)
admin.site.register(BlogModel)
