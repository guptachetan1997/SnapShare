from django.forms import ModelForm
from posts.models import Post


class PostForm(ModelForm):
	class Meta:
		model = Post
		fields = ('caption', 'image')
	
	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		self.fields['caption'].required = False