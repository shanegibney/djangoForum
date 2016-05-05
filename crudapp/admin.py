from django.contrib import admin
from .models import Members, TopicModel, PostModel
# from .forms import NameForm

# Register your models here.
admin.site.register(Members)
admin.site.register(TopicModel)
admin.site.register(PostModel)
