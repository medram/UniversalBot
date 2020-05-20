from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from background_task.models import Task, CompletedTask

from .models import List, Profile, Proxy, TaskAdaptor, Server

APP_NAME = 'Universal Bot'

admin.site.site_title = f'{APP_NAME} v0.1.0'
admin.site.site_header = f'{APP_NAME} v0.1.0'
admin.site.index_title = 'Dashboard'


admin.site.unregister(Task)
admin.site.unregister(CompletedTask)

############## Actions ##############
def activate_all_profiles(modeladmin, request, queryset):
	queryset.update(status=True)
activate_all_profiles.short_description = 'Activate'

def deactivate_all_profiles(modeladmin, request, queryset):
	queryset.update(status=False)
deactivate_all_profiles.short_description = 'Deactivate'

#####################################


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'email', 'status', 'updated', 'created')
	list_display_links = ('id', 'email')
	list_per_page = 25
	# list_editable = ('status',)
	list_filter = ('status', 'created')
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



@admin.register(TaskAdaptor)
class TaskAdaptorAdmin(admin.ModelAdmin):
	fields = ('task_name', 'run_at', 'repeat', 'repeat_until', 'lists', 'servers')
	filter_horizontal = ('lists', 'servers')

	list_display = ('id', 'task_name', 'run_at', 'repeat', 'repeat_until', 'count_lists', 'created', 'is_completed', 'show_progress')
	list_display_links = ('task_name',)
	list_per_page = 25
	list_filter = ('created', 'repeat')
	search_fields = ('id', 'task_name')

	def show_progress(self, obj):
		if obj.progress:
			return f'{obj.progress:0.02f}%'
		return '-'
	show_progress.short_description = 'Progress (%)'

	def count_lists(self, obj):
		return f'{obj.lists.count()} list(s)'
	count_lists.short_description = 'Lists'

	def is_completed(self, obj):
		return bool(not obj.task and obj.completed_task)
	is_completed.boolean = True
	is_completed.short_description = 'Completed'


############## Actions ##############
def activate_all_ips(modeladmin, request, queryset):
	queryset.update(active=True)
activate_all_ips.short_description = 'Activate'

def deactivate_all_ips(modeladmin, request, queryset):
	queryset.update(active=False)
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
	list_display = ('ip', 'port', 'capacity','active', 'created')
	list_per_page = 25
	search_fields = ('ip', 'port')
	list_filter = ('created', 'active')
	actions = (activate_all_ips, deactivate_all_ips)
