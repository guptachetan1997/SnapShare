from django.contrib import admin
from posts.models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
	readonly_fields = ('timestamp', 'uuid')

admin.site.register(Post, PostAdmin)
