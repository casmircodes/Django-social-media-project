from .models import Follow


def follow_user(followed, follower):
	if Follow.objects.filter(followed_user=followed, follower_user=follower).exists():
		Follow.objects.filter(followed_user=followed, follower_user=follower).first().delete()
		#return redirect(return_page)
	else:
		new_follow = Follow.objects.create(followed_user=followed, follower_user=follower)
		new_follow.save()
		#return redirect(return_page)





"""

if Follow.objects.filter(followed_user=username, follower_user=request.user.username).exists():
			Follow.objects.filter(followed_user=username, follower_user=request.user.username).first().delete()
			return redirect("/profile/"+username+"/")

		else:
			new_follow = Follow.objects.create(followed_user=username, follower_user=request.user.username)
			new_follow.save()
			return redirect("/profile/"+username+"/")

"""