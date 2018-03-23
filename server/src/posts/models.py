import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def upload_location(instance, filename):
	new_file_name = "{}.{}".format(str(instance.uuid), filename.split('.')[-1])
	return "posts/{}".format(new_file_name)


class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	caption = models.CharField(max_length = 100, blank=True, null=True)
	image = models.ImageField(upload_to=upload_location)
	timestamp = models.DateTimeField(auto_now_add=True)
	uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	tags = models.CharField(max_length=500, blank=True, null=True)

	def check_like(self, user):
		try:
			Like.objects.get(user=user, post=self)
			return 1
		except:
			return 0
	
	@property
	def comments_count(self):
		return Comment.objects.filter(post=self).count()

	@property
	def likes_count(self):
		return Like.objects.filter(post=self).count()
	
	def add_comment(self, from_user, text):
		try:
			from_user_obj = User.objects.get(username = from_user)
			comment = Comment.objects.create(user=from_user_obj, post=self, text=text)
			if comment:
				return True
			else:
				return False
		except:
			return False

	def toggle_like(self, from_user):
		try:
			from_user_obj = User.objects.get(username = from_user)
		except:
			return {"status" : False}

		if from_user_obj:
			try:
				like_obj = Like.objects.get(user=from_user_obj, post=self)
				like_obj.delete()
				return {"status" : True, "like_flag" : False}
			except:
				Like.objects.create(post=self, user=from_user_obj)
				return {"status" : True, "like_flag" : True}


	def __str__(self):
		return str("{}  [{}]".format(self.uuid, self.timestamp))


class Like(models.Model):
	timestamp = models.DateTimeField(auto_now=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
	timestamp = models.DateTimeField(auto_now=True)
	text = models.CharField(max_length=500)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)

	def __str__(self):
		return "{} {}".format(self.post.id, self.post.user.username)