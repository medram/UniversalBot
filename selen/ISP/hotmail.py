import time
import json
import os

from django.conf import settings
from json.decoder import JSONDecodeError

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
		NoSuchElementException,
		ElementClickInterceptedException
	)


from .abstract import AbstractISP
from .. import exceptions

class Hotmail(AbstractISP):

	def login(self):
		print('Login')
		# check the login status.
		# try to login if we are not.
		# create profile if the account is new.
		self._load_cookies()
		self._automatic_login()
		self._save_cookies()

		self.driver.get('https://outlook.live.com/mail/0/inbox')

	def do_actions(self):
		pass

	def create_profile(self):
		print('creating profile.')

	def _load_cookies(self):
		try:
			with open(os.path.join(settings.MEDIA_ROOT, f'profile_cookies/{self.profile.email}.json')) as f:
				cookies = json.load(f)
				for i, cookie in enumerate(cookies):
					print('>', i)
					print(cookie)
					self.driver.add_cookie(cookie)
				print('Cookies is loaded.')
		except (FileNotFoundError, JSONDecodeError):
			pass


	def _save_cookies(self):
		with open(os.path.join(settings.MEDIA_ROOT, f'profile_cookies/{self.profile.email}.json'), 'w') as f:
			json.dump(self.driver.get_cookies(), f, indent=2)
			print('Cookies is saved.')


	def _automatic_login(self):
		self.driver.get('https://login.live.com')
		self.driver.implicitly_wait(3)

		# https://account.microsoft.com (redirected to this url if it's logged in)
		# check the login.
		if not self.driver.current_url.startswith('https://account.microsoft.com'):
			self.loggedin = False
			print('[Info] {} (automatic login...).'.format(self.profile.email))

			email = self.driver.find_element_by_id("i0116")
			email.clear()
			email.send_keys(self.profile.email)
			email.send_keys(Keys.RETURN)

			time.sleep(1)

			password = self.driver.find_element_by_id('i0118')
			password.clear()
			password.send_keys(self.profile.password)
			try:
				checkbox = self.driver.find_element_by_css_selector('label#idLbl_PWD_KMSI_Cb').click()
			# except (NoSuchElementException, ElementClickInterceptedException):
			except:
				pass
			
			time.sleep(1)
			# Click login
			password.send_keys(Keys.RETURN)		
			time.sleep(2)

			# check the login status.
			wait = WebDriverWait(self.driver, 20, poll_frequency=0.05)
			if not wait.until(EC.url_contains('https://account.microsoft.com')):
				print('[Info] {} (May need a manual login).'.format(self.profile.email))
				raise exceptions.CantLogin()

			# report that we are logged in :D
			self.loggedin = True
		else:
			# report that we are logged in :D
			self.loggedin = True
