from django.shortcuts import render, redirect
from django.core import serializers

# Create your views here.
from background_task import background
from django.contrib.auth.models import User

def home(req):
	return redirect('/admin')
	# return render(req, 'universalbot/index.html')