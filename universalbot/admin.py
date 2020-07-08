from django.contrib import admin, messages
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from background_task.models import Task, CompletedTask
from selen.manager import ApprovedTaskManager

from .models import List, Profile, Proxy, TaskAdaptor, Server, ATM


admin.site.site_title = f'{settings.APP_NAME}'
admin.site.site_header = f'{settings.APP_NAME}'
admin.site.index_title = 'Dashboard'

admin.site.unregister(Task)
admin.site.unregister(CompletedTask)

############## Actions ##############
def activate_all_profiles(modeladmin, request, queryset):
	queryset.update(status=True)
	modeladmin.message_user(request, f'Selected profiles are activated successfully.', messages.SUCCESS)
activate_all_profiles.short_description = 'Activate'

def deactivate_all_profiles(modeladmin, request, queryset):
	queryset.update(status=False)
	modeladmin.message_user(request, f'Selected profiles are deactivated successfully.', messages.SUCCESS)
deactivate_all_profiles.short_description = 'Deactivate'

#####################################


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'email', 'status', 'updated', 'created')
	list_display_links = ('id', 'email')
	list_per_page = 50
	# list_editable = ('status',)
	list_filter = ('status', 'created', 'list')
	search_fields = ('email', 'id')
	actions = (activate_all_profiles, deactivate_all_profiles)


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
	# at CRUD
	list_display = ('id', 'name', 'count_profiles', 'show_actions', 'updated', 'created')
	list_display_links = ('name',)
	list_per_page = 25
	list_filter = ('actions', 'created')
	search_fields = ('id', 'name')
	date_hierarchy = 'created'

	# at adding or editting
	fields = ('name', 'file', 'profiles', 'actions')
	filter_horizontal = ('profiles',)


	def count_profiles(self, obj):
		return f'{obj.profiles.count()} profile(s)'
	count_profiles.short_description = 'Added Profiles'

	def show_actions(self, obj):
		return f'{len(obj.actions)} action(s)'
	show_actions.short_description = 'Actions'


############## Actions ##############
def clear_queue(modeladmin, request, queryset):
	task_adapters = queryset.all()
	try:
		for task_adapter in task_adapters:
			ApprovedTaskManager.register_queue_deletion(task_adapter)
	except Exception:
		modeladmin.message_user(request, f'Oops! something went wrong.', messages.ERROR)
	else:
		modeladmin.message_user(request, f'Selected Task Queues are cleared successfully.', messages.SUCCESS)
clear_queue.short_description = 'Clear Task Queues'


@admin.register(TaskAdaptor)
class TaskAdaptorAdmin(admin.ModelAdmin):
	fields = ('task_name', 'run_at', 'repeat', 'repeat_until', 'lists', 'servers')
	filter_horizontal = ('lists', 'servers')

	list_display = ('id', 'task_name', 'run_at', 'repeat', 'repeat_until', 'count_lists', 'total_profiles',
		'created', 'get_queue_status', 'show_progress')
	list_display_links = ('task_name',)
	list_per_page = 25
	list_filter = ('created', 'repeat', 'queue_status')
	search_fields = ('id', 'task_name')
	actions = (clear_queue,)
	date_hierarchy = 'created'

	def show_progress(self, obj):

		# all_profiles = sum([ l.profiles.filter(status=True).count() for l in obj.lists.all() ])
		if obj.queue_status == obj.QUEUE_STATUS.PROCESSING and obj.total_qsize:
			try:
				progress = round((obj.total_qsize - obj.qsize) / obj.total_qsize * 100, 2)
			except ZeroDivisionError:
				progress = 0
			return mark_safe(f'<small>{progress:0.02f}% ({obj.qsize} in queue)</small>')

		return '-'
	show_progress.short_description = 'Progress (%)'


	def total_profiles(self, obj=None):
		return '%d profiles' % sum([ l.profiles.filter(status=True).count() for l in obj.lists.all() ])


	def get_queue_status(self, obj=None):
		if obj.queue_status == obj.QUEUE_STATUS.COMPLETED:
			return mark_safe(f'<span class="badge badge-pill badge-success">{obj.get_queue_status_display().upper()}</span>')
		elif obj.queue_status == obj.QUEUE_STATUS.PROCESSING:
			return mark_safe(f'<span class="badge badge-pill badge-warning">{obj.get_queue_status_display().upper()}...</span>')
		return mark_safe(f'<span class="badge badge-pill badge-secondary">{obj.get_queue_status_display().upper()}</span>')

	get_queue_status.short_description = 'Queue status'


	def count_lists(self, obj=None):
		return f'{obj.lists.count()} lists'
	count_lists.short_description = 'Lists'

	def is_completed(self, obj):
		return bool(not obj.task and obj.completed_task)
	is_completed.boolean = True
	is_completed.short_description = 'Completed'


############## Actions ##############
def activate_all_ips(modeladmin, request, queryset):
	queryset.update(active=True)
	modeladmin.message_user(request, f'Selected IPs are activated successfully.', messages.SUCCESS)
activate_all_ips.short_description = 'Activate'

def deactivate_all_ips(modeladmin, request, queryset):
	queryset.update(active=False)
	modeladmin.message_user(request, f'Selected IPs are deactivated successfully.', messages.SUCCESS)
deactivate_all_ips.short_description = 'Deactivate'

#####################################

@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):
	list_display = ('ip', 'port', 'proxy_type', 'active', 'default', 'created')
	list_per_page = 25
	search_fields = ('ip', 'port')
	list_filter = ('created', 'active', 'default')
	# list_editable = ('default',)
	actions = (activate_all_ips, deactivate_all_ips)
	fields = ('ip', 'port', 'proxy_type','active', 'default')


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
	list_display = ('ip', 'port', 'name', 'capacity','active', 'created')
	list_per_page = 25
	search_fields = ('name', 'ip', 'port')
	list_filter = ('created', 'active')
	actions = (activate_all_ips, deactivate_all_ips)


# @admin.register(ATM)
# class ATMAdmin(admin.ModelAdmin):
# 	pass
