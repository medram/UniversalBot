import time
import json
import os
# import pickle

from django.conf import settings
from json.decoder import JSONDecodeError

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
		NoSuchElementException,
		ElementClickInterceptedException,
		InvalidCookieDomainException,
		StaleElementReferenceException
	)


from selen.abstract import AbstractISP, ActionAbstract
from selen import exceptions, utils
from universalbot.models import Actions
from .actions import Inbox_select_all_mark_as_read, Spam_select_all_mark_as_read


class Hotmail(AbstractISP):

	def do_actions(self):
		if self.loggedin:

			self.driver.get('https://outlook.live.com/mail/0/inbox')
			self.driver.implicitly_wait(4)

			with utils.document_completed(self.driver, 20):
				# let javascript requests finish.
				time.sleep(15)
				
				for action in self.list.actions: # action is a str number
					try:
						ActionObject = self.actions[Actions(int(action))]
						if isinstance(ActionObject, ActionAbstract):
							ActionObject.apply()
					except KeyError:
						pass


	def register_actions(self):
		print('register actions')
		self.actions[Actions.INBOX_SELECT_ALL_MARK_AS_READ] = Inbox_select_all_mark_as_read(self)
		self.actions[Actions.SPAM_SELECT_ALL_MARK_AS_READ] = Spam_select_all_mark_as_read(self)


	def login(self):
		print('Login')
		self._automatic_login()


	def logout(self):
		pass


	def create_profile(self):
		print('creating profile.')


	def _load_cookies(self):
		# self.driver.get('https://google.com')
		try:
			cookie_path = os.path.join(settings.MEDIA_ROOT, f'profile_cookies/{self.profile.email}.pkl')
			with open(cookie_path, 'r') as f:
				# cookies = pickle.load(f)
				cookies = json.load(f)
				for cookie in cookies:
					try:
						self.driver.add_cookie(cookie)
					except InvalidCookieDomainException as e:
						print(e)
					else:
						print(f"> cookie is loaded: {cookie['domain']}")
				print('Cookies are loaded.')
		except (FileNotFoundError, JSONDecodeError) as e:
			print(e)


	def _save_cookies(self):
		time.sleep(3)
		print('_save_cookies')
		cookie_path = os.path.join(settings.MEDIA_ROOT, f'profile_cookies/{self.profile.email}.pkl')
		with open(cookie_path, 'r+') as f:
			for c in self.driver.get_cookies():
				print(c['domain'])

			cookies = json.load(f)
			# pickle.dump(self.driver.get_cookies(), f)
			json.dump(cookies.extend(self.driver.get_cookies()), f, indent=2)
			print('Cookies is saved.')


	def _automatic_login(self):
		self.driver.get('https://login.live.com')
		self.driver.implicitly_wait(3)

		# https://account.microsoft.com (redirected to this url if it's logged in)
		# check the login.
		if not self.driver.current_url.startswith('https://account.microsoft.com'):
			self.loggedin = False
			print('[Info] {} (automatic login...).'.format(self.profile.email))

			time.sleep(1)

			email = self.driver.find_element_by_id("i0116")
			email.clear()
			email.send_keys(self.profile.email)
			email.send_keys(Keys.RETURN)

			self.driver.implicitly_wait(2)
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
			try:
				password.send_keys(Keys.RETURN)
			except StaleElementReferenceException:
				self.driver.find_element_by_css_selector('input[type=submit]').click()

			self.driver.implicitly_wait(2)
			# time.sleep(1)

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
