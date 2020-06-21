from django.contrib import admin
from universalbot.models import Server, Profile, Proxy, TaskAdaptor, ATM

# My custom AdminSite
class MyAdminSite(admin.AdminSite):

	def index(self, request, extra_context=None):
		if extra_context is None:
			extra_context = {}
		# Adding my context here
		extra_context.update({
			'servers': Server.objects.count(),
			'profiles': Profile.objects.count(),
			'proxies': Proxy.objects.count(),
			'queues': ATM.objects.count(),
			'tasks': TaskAdaptor.objects.count(),
			'workers': sum(( s.capacity for s in Server.objects.filter(active=True).all() ))
		})
		return super().index(request, extra_context=extra_context)