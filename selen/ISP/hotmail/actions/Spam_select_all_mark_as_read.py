import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


from selen.abstract import ActionAbstract
from selen import utils

class Spam_select_all_mark_as_read(ActionAbstract):

	def apply(self):
		print(f'Firing Action: {self.__class__.__name__}...')
		driver = self.isp.driver

		# print('Start ActionChains...')
		# Go to Junk section
		driver.get('https://outlook.live.com/mail/junkemail')

		with utils.document_completed(driver, 20):
			# let javascript requests finish.
			time.sleep(5)

			actions = ActionChains(driver)
			# Select all messages.
			actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
			time.sleep(2)
			# print('select all')
			# mark all as read.
			actions.send_keys('q').perform()
			# print('mark all')

			wait = WebDriverWait(driver, 15)
			try:
				if wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.ms-Dialog-actionsRight'))):
					# mark all as read
					# print('Confirm')
					actions.send_keys(Keys.RETURN).perform()
					# wait to make sure the action is applied
					time.sleep(2)
			except TimeoutException:
				print(f'{self.__class__.__name__} not granted')