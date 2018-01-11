""" Models for the accounts app. """
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

def upload_location(instance, filename):
	u = User.objects.get(id = instance.user_id)
	return "{}/{}".format(str(u.username), filename)


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(max_length = 500, null=True, blank=True)
	profile_picture = models.ImageField(null=True, blank=True, upload_to=upload_location, default='/default_user_image.jpg')

	def __str__(self):
		return self.user.username + "'s profile."

	@property
	def get_full_name(self):
		return "{} {}".format(self.user.first_name, self.user.last_name)

	def toggle_connection(self, to_user):
		try:
			_to_user = User.objects.get(username = to_user)
			if _to_user:
				try:
					conn = Connection.objects.get(from_user=self.user, to_user=_to_user)
					conn.delete()
					return {"status" : True, "following_flag" : False}
				except Connection.DoesNotExist:
					Connection.objects.create(from_user=self.user, to_user=_to_user)
					return {"status" : True, "following_flag" : True}
		except Exception as e:
			print(e)
			return {"status" : False}

	def check_connection(self, to_user):
		flag = Connection.objects.filter(from_user = self.user, to_user=to_user).count()
		return flag > 0

	def get_connections(self):
		connections = Connection.objects.filter(from_user=self.user)
		return connections

	def get_followers(self):
		followers = Connection.objects.filter(to_user=self.user)
		return followers

	@property
	def connection_count(self):
		return self.get_connections().count()
	
	@property
	def follower_count(self):
		return self.get_followers().count()


class Connection(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	from_user = models.ForeignKey(User, related_name="creator_set", on_delete=models.CASCADE)
	to_user = models.ForeignKey(User, related_name="friend_set", on_delete=models.CASCADE)

	class Meta:
		unique_together = ("from_user", "to_user")

	def __str__(self):
		return "{} follows {}".format(self.from_user.username, self.to_user.username)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()