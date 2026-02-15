from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, LikedPost, Follow
from django.contrib.auth import login as login_user
from django.contrib.auth import authenticate
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
import uuid
from itertools import chain
from .followuser import follow_user
import random

# Create your views here.
@login_required(login_url="/login/")
def index(request):
	profile = Profile.objects.filter(user=request.user).first()
	#all_posts = Post.objects.all()
	objects_the_loggedin_user_follows = Follow.objects.filter(follower_user=request.user.username)
	posts = []

	for object_the_loggedin_user_follows in objects_the_loggedin_user_follows:
		posts_of_a_user_followed_by_loggedin_user = Post.objects.filter(username=object_the_loggedin_user_follows.followed_user)
		posts.append(posts_of_a_user_followed_by_loggedin_user)

	all_post_objs = list(chain(*posts))

	follow_objects_where_loggedin_user_is_a_follower = Follow.objects.filter(follower_user=request.user.username)
	profiles_loggedin_user_follows = []

	for follow_object_where_loggedin_user_is_a_follower in follow_objects_where_loggedin_user_is_a_follower:
		user = User.objects.filter(username=follow_object_where_loggedin_user_is_a_follower.followed_user).first()
		profile = Profile.objects.filter(user=user).first()
		profiles_loggedin_user_follows.append(profile)


	all_profiles = Profile.objects.all()
	profiles_loggedin_user_doesnot_follow = []

	for prof in all_profiles:
		if prof not in profiles_loggedin_user_follows and prof.user.username != request.user.username:
			profiles_loggedin_user_doesnot_follow.append(prof)

	random.shuffle(profiles_loggedin_user_doesnot_follow)




	return render(request, "index.html", {"profile": profile, "posts": all_post_objs, "profiles": profiles_loggedin_user_doesnot_follow[:5]})


@login_required(login_url="/login/")
def profile(request, username):
	if Follow.objects.filter(followed_user=username, follower_user=request.user.username).exists():
		follow_text = "UnFollow"

	else:
		follow_text = "Follow"

	user = User.objects.filter(username=username).first()
	profile = Profile.objects.filter(user=user).first()
	posts = Post.objects.filter(username=username)
	followed = Follow.objects.filter(followed_user=username)
	follower = Follow.objects.filter(follower_user=username)

	post_length = len(posts)
	followers = len(followed)
	followings = len(follower)

	post_images = []
	for post in posts:
		post_images.append(post.post_image.url)



	context = {
	"follow_text": follow_text, 
	"followed_user": username,
	"username": username,
	"bio": profile.bio,
	"profile_pics": profile.profile_image.url,
	"post_length": post_length,
	"post_images": post_images,
	"followers": followers,
	"followings": followings

	}
	return render(request, "profile.html", context )

@login_required(login_url="/login/")	
def follow(request, username):
	if request.method == "POST":
		redirectpage = request.POST.get("redirectpage")
		if redirectpage == "index":
			follow_user(username, request.user.username)
			return redirect("/")
		else:
			follow_user(username, request.user.username)
			return redirect("/profile/"+username+"/")

			



@login_required(login_url="/login/")
def search(request):
	loggedin_user = User.objects.filter(username=request.user.username).first()
	loggedin_user_profile = Profile.objects.filter(user=loggedin_user).first() 

	if request.method == "POST":
		username = request.POST.get("username")
		users = User.objects.filter(username__icontains=username)
		profile_objects = []
		
		for user in users:
			profile = Profile.objects.filter(user=user).first()
			profile_objects.append(profile)
		#print(profile_objects)
		#return redirect("/search/")

	return render(request, "search.html", {"searched_profiles": profile_objects, "loggedin_user_profile": loggedin_user_profile})




@login_required(login_url="/login/")
def comment(request):
	if request.method == "POST":
		comment_text = request.POST.get("comment")
		parent_post_id = request.POST.get("postid")
		parent_post_id = uuid.UUID(parent_post_id)
		post = Post.objects.filter(post_id=parent_post_id).first()
		profile = Profile.objects.filter(user=request.user).first()
		new_comment = Comment.objects.create(parent_post=post, comment_author=request.user.username, comment_text=comment_text, comment_author_profile_picture=profile.profile_image.url)
		new_comment.save()
		return redirect("index")


@login_required(login_url="/login/")
def liked_post(request, postid):
	post = Post.objects.filter(post_id=postid).first()
	if LikedPost.objects.filter(post_id=postid, liking_user_username=request.user.username).exists():
		LikedPost.objects.filter(post_id=postid, liking_user_username=request.user.username).first().delete()
		post.no_of_likes = post.no_of_likes - 1
		post.save()
		return redirect("/")

	else:
		likedpost = LikedPost.objects.create(post_id=postid, liking_user_username=request.user.username)
		post.no_of_likes = post.no_of_likes + 1
		post.save()
		return redirect("/")


	#return HttpResponse("khdhdjhg")





@login_required(login_url="/login/")
def upload(request):
	if request.method == "POST":
		photo = request.FILES.get("photo")
		caption = request.POST.get("caption")
		user = User.objects.filter(username=request.user.username).first()
		profile = Profile.objects.filter(user=user).first()
		new_post = Post.objects.create(username=request.user.username, post_image=photo, caption=caption, image_of_author=profile.profile_image.url)
		new_post.save()

	return redirect("/")



@login_required(login_url="/login/")
def settings(request):
	profile = Profile.objects.filter(user=request.user).first()


	if request.method == 'POST':

		profile_image = request.FILES.get("profileimage")
		bio = request.POST.get('bio')
		location = request.POST.get('location')
		if request.FILES.get("profileimage") != None:
			
			profile.profile_image = profile_image
			profile.bio = bio
			profile.location = location
			profile.save()
			messages.info(request, "Your profile update is successful!")
			#return redirect("/settings/")

		else:
			profile.bio = bio
			profile.location = location
			profile.save()
			messages.info(request, "Your profile has been successfully updated!")
			#return redirect("/settings/")


	return render(request, "setting.html", {"profile": profile})


def register(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		password2 = request.POST.get('password2')

		if password == password2:

			if User.objects.filter(username=username).exists():
				messages.info(request, 'Username already exists!')

			elif User.objects.filter(email=email).exists():
				messages.info(request, 'Email already exists!')

			else:
				user = User.objects.create_user(username=username, email=email, password=password)
				profile = Profile.objects.create(user=user, profile_id=user.id)
				profile.save()

				login_user(request, user)
				return redirect('/settings/')




		else:
			messages.info(request, 'Your first and second password did not match.')


	return render(request, "signup.html")


def login(request):
	if request.method == 'POST':
		username = request.POST.get("username")
		password = request.POST.get("password")

		user = authenticate(request, username=username, password=password)

		if user != None:
			login_user(request, user)
			return redirect("/")
		else:
			messages.info(request, "Incorrect email or password.")

	return render(request, "signin.html")



def logout(request):
	if request.method == "POST":
		logout_user(request)
		return redirect("/login/")