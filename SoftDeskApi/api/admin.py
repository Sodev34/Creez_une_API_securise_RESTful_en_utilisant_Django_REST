from django.contrib import admin
from .models import Projects, Issues, Contributors, Comments


admin.site.register(Projects)
admin.site.register(Issues)
admin.site.register(Contributors)
admin.site.register(Comments)

