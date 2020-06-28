import os
from . app_settings import FIREFOX_PROFILES_PATH


class Singleton:
	def __init__(self, cls):
		self._cls = cls

	def get_instance(self):
		try:
			return self._instance
		except AttributeError:
			self._instance = self._cls()

		return self._instance

	def __call__(self):
		raise TypeError('Singletons must be accessed through `get_instance()`.')

	def __instancecheck__(self, inst):
		return isinstance(inst, self._cls)


def get_profiles_paths():
	return [
            os.path.join(FIREFOX_PROFILES_PATH, d) for d in os.listdir(FIREFOX_PROFILES_PATH)
            if os.path.isdir(os.path.join(FIREFOX_PROFILES_PATH, d))
            and 'default' not in d
        ]
