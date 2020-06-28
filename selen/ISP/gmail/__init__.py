import time
import json
import os
# import pickle

from django.conf import settings
from json.decoder import JSONDecodeError

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
		NoSuchElementException,
		ElementClickInterceptedException,
		InvalidCookieDomainException,
		StaleElementReferenceException,
		TimeoutException
	)


from selen.abstract import AbstractISP, ActionAbstract
from selen import exceptions, utils
from universalbot.models import Actions
from .actions import (
		Inbox_archive_all,
	)


class Gmail(AbstractISP):

	def do_actions(self):
		if self.loggedin:
			# self.driver.get('https://outlook.live.com/mail/0/inbox')
			# self.driver.implicitly_wait(4)
			time.sleep(1)

			with utils.page_is_loaded(self.driver, EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div#loading'))):
				# let javascript requests finish.
				time.sleep(3)
				
				for action in self.list.actions: # action is a str number
					try:
						ActionObject = self.actions[Actions(int(action))]
						if isinstance(ActionObject, ActionAbstract):
							ActionObject.apply()
					except KeyError:
						pass
					except Exception as e:
						print(e)


	def register_actions(self):
		self.actions[Actions.INBOX_ARCHIVE_ALL] = Inbox_archive_all(self)


	def login(self):
		if self.is_created_profile_used:
			self.loggedin = True
		else:
			self._automatic_login()



	def logout(self):
		pass


	def create_profile(self):
		print('creating profile.')



	def _automatic_login(self):
		self.driver.get('https://gmail.com')
		self.driver.implicitly_wait(3)
		time.sleep(1)
		# https://account.microsoft.com (redirected to this url if it's logged in)
		# check the login.
		if not self.driver.current_url.startswith('https://mail.google.com/mail'):
			self.loggedin = False
			self.driver.implicitly_wait(3)
			time.sleep(1)
			
			email = self.driver.find_element_by_css_selector("input[type=email]")
			email.clear()
			email.send_keys(self.profile.email)
			email.send_keys(Keys.RETURN)

			self.driver.implicitly_wait(3)
			time.sleep(1)

			password = self.driver.find_element_by_css_selector("input[type=password]")
			password.clear()
			password.send_keys(self.profile.password)

			# Click login
			try:
				password.send_keys(Keys.RETURN)
			except StaleElementReferenceException:
				self.driver.find_element_by_css_selector('div#passwordNext').click()

			self.driver.implicitly_wait(2)
			time.sleep(2)

			# check the login status.
			try:
				wait = WebDriverWait(self.driver, 30, poll_frequency=0.05)
				wait.until(EC.url_contains('https://mail.google.com/mail'))
			except TimeoutException:
				raise exceptions.CantLogin()
			else:
				# report that we are logged in :D
				self.loggedin = True
		else:
			# report that we are logged in :D
			self.loggedin = True
