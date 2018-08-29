from django.contrib import admin
from posts.models import Post, Comment, Tag, PostTagBridge

# Register your models here.

class PostAdmin(admin.ModelAdmin):
	readonly_fields = ('timestamp', 'uuid')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(PostTagBridge)
