from django.contrib import admin

from django.conf import settings

from extra_settings.models import Setting
from extra_settings.admin import SettingAdmin
from extra_settings.apps import ExtraSettingsConfig

admin.site.unregister(Setting)

ExtraSettingsConfig.verbose_name = 'Settings'
# ExtraSettingsConfig.name = 'settings'

@admin.register(Setting)
class SettingAdmin(SettingAdmin):
	list_filter = ()
	
	def get_readonly_fields(self, req, obj=None):
		return ('name', 'value_type') if obj else ()

	def has_delete_permission(self, req, obj=None):
		return settings.DEBUG

	def has_add_permission(self, req, obj=None):
		return settings.DEBUG