from django.contrib import admin
from .models import List, Profile, Proxy, TaskAdaptor

admin.site.site_title = 'HotmailBot v0.1.0'
admin.site.site_header = 'HotmailBot v0.1.0'
admin.site.index_title = 'Dashboard'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'email', 'updated', 'created')
	list_display_links = ('id', 'email')
	list_per_page = 25

	list_filter = ('status', 'created')
	search_fields = ('email', 'id')


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
	# at CRUD
	list_display = ('id', 'name', 'count_profiles', 'show_actions', 'updated', 'created')
	list_display_links = ('name',)
	list_per_page = 25
	list_filter = ('actions', 'created')
	search_fields = ('id', 'name')

	# at adding or editting
	fields = ('name', 'file', 'profiles', 'actions')	
	filter_horizontal = ('profiles',)

	def count_profiles(self, obj):
		return f'{obj.profiles.count()} profile(s)'
	count_profiles.short_description = 'Added Profiles'

	def show_actions(self, obj):
		return f'{len(obj.actions)} action(s)'
	show_actions.short_description = 'Actions'


@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):
	pass


@admin.register(TaskAdaptor)
class TaskAdaptorAdmin(admin.ModelAdmin):
	filter_horizontal = ('lists',)
	fields = ('task_name', 'run_at', 'repeat', 'repeat_until', 'lists')
	# task name, task params, task hash

	list_display = ('id', 'task_name', 'run_at', 'repeat', 'repeat_until', 'count_lists', 'created')
	list_display_links = ('task_name',)
	list_filter = ('created', 'repeat')
	search_fields = ('id', 'task_name')

	def count_lists(self, obj):
		return f'{obj.lists.count()} list(s)'
	count_lists.short_description = 'Lists'


# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
# 	list_display = ('id', 'name', 'count_lists', 'start', 'status', 'created')
# 	list_display_links = ('id', 'name')
# 	list_editable = ('status',)
# 	list_per_page = 25

# 	list_filter = ('created', 'status')
# 	search_fields = ('id', 'name')
# 	filter_horizontal = ('lists',)

# 	def count_lists(self, obj):
# 		return f'{obj.lists.count()} list(s)'
# 	count_lists.short_description = 'Affected Lists'
