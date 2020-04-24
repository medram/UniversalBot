from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoAlertPresentException, NoSuchElementException, 
	TimeoutException)
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

from selen import exceptions

# automatic login
def automaticLogin(driver, profile):
	if driver.current_url.startswith('https://login.live.com'):
		print('[warning] {email} (automatic login...).'.format(profile.email))

		email = driver.find_element_by_id("i0116")
		email.clear()
		email.send_keys(profile.email)
		email.send_keys(Keys.RETURN)

		driver.implicitly_wait(1)

		password = driver.find_element_by_id('i0118')
		password.clear()
		password.send_keys(profile.password)
		checkbox = driver.find_element_by_css_selector('input[name=KMSI]').click()
		password.send_keys(Keys.ENTER)

		driver.implicitly_wait(2)

		if not driver.current_url.startswith('https://outlook.live.com/mail'):
			print('[warning] {email} (May need a manual login).'.format(profile.email))
			raise exceptions.CantLogin()

class MyListeners(AbstractEventListener):
	def before_close(self, driver):
		print('fire before close function.')

	def before_quit(self, driver):
		print('fire before quit function.')
		# with open('cookies/test.cks', 'w') as f:
		# 	json.dump(driver.get_cookies(), f, indent=2)
		# shutil.rmtree(profile_path, ignore_errors=True)
		# shutil.copytree(driver.firefox_profile.path, profile_path)


def CreateProfile(profile):
	"""
	Create a new profile.
	"""
	print('Create profile')
	# fp = webdriver.FirefoxProfile()
	# driver = webdriver.Firefox(
	# 	fp,
	# 	executable_path=settings.EXECUTABLE_PATH, 
	# 	service_log_path=settings.LOGS_PATH
	# 	# log_path = log_path
	# 	)

	# driver = EventFiringWebDriver(driver, MyListeners())

	# driver.get('https://outlook.live.com/mail/0/inbox')
	# driver.implicitly_wait(2)

	# # automatic login (CantLogin exception)
	# automaticLogin(driver, profile)




