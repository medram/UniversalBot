from django.shortcuts import render
from django.core import serializers

# Create your views here.
from background_task import background
from django.contrib.auth.models import User

@background(schedule=5)
def notify_user(user_id):
    # lookup user by id and send them a message
    print(f'>> notify_user is fired (user: {user_id})')

def home(req):
	# user = serializers.serialize('json', req.user)
	notify_user(req.user.pk)
	return render(req, 'universalbot/index.html')