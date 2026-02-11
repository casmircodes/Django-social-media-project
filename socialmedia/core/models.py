from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

	profile_image = models.ImageField(upload_to="profile_images", default="profile_images/blank-profile-picture.png")

	profile_id = models.IntegerField()

	location = models.CharField(max_length=200, blank=True)

	bio = models.TextField(blank=True)

	def __str__(self):

		return self.user.username



class Post(models.Model):
	username = models.CharField(max_length=255)
	post_image = models.ImageField(upload_to="post_images")
	caption = models.TextField()
	post_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	no_of_likes = models.IntegerField(default=0)
	posted_on = models.DateTimeField(auto_now_add=True)
	image_of_author = models.CharField(max_length=255, null=True)

	def __str__(self):
		return self.username


class Comment(models.Model):
	parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
	comment_author = models.CharField(max_length=255)
	comment_text = models.CharField(max_length=255)
	comment_author_profile_picture = models.CharField(max_length=255)


class LikedPost(models.Model):
	post_id = models.UUIDField()
	liking_user_username = models.CharField() 


class Follow(models.Model):
	follower_user = models.CharField()
	followed_user = models.CharField()