import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def upload_location(instance, filename):
	new_file_name = "{}.{}".format(str(instance.uuid), filename.split('.')[-1])
	return "posts/{}".format(new_file_name)


class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	caption = models.CharField(max_length = 100, blank=True, null=True)
	image = models.ImageField(upload_to=upload_location)
	timestamp = models.DateTimeField(auto_now_add=True)
	uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

	def check_like(self, user):
		try:
			Like.objects.get(user=user, post=self)
			return 1
		except:
			return 0
	
	@property
	def get_tags(self):
		tags = PostTagBridge.objects.filter(post = self)
		return [x.tag for x in tags]
	
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
	
	def add_tag(self, tag_text):
		try:
			tag_obj = Tag.objects.get(text=tag_text)
		except Tag.DoesNotExist:
			tag_obj = Tag(text=tag_text)
			tag_obj.save()
		try:
			post_tag_bridge_obj = PostTagBridge(tag=tag_obj, post=self)
			post_tag_bridge_obj.save()
			return True
		except:
			return False

	def __str__(self):
		return str("{}  [{}]".format(self.uuid, self.timestamp))


class Tag(models.Model):
	text = models.CharField(max_length=100)

	@property
	def count(self):
		return PostTagBridge.objects.filter(tag=self).count()
	
	@property
	def most_recent_post(self):
		return PostTagBridge.objects.filter(tag=self).order_by("-created_on").first().post

	def __str__(self):
		return "{}".format(self.text)


class PostTagBridge(models.Model):
	created_on = models.DateTimeField(auto_now=True)
	tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="tag_name")
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="tagged_post")


class Like(models.Model):
	timestamp = models.DateTimeField(auto_now=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")


class Comment(models.Model):
	timestamp = models.DateTimeField(auto_now=True)
	text = models.CharField(max_length=500)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)

	def __str__(self):
		return "{} {}".format(self.post.id, self.post.user.username)