import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


from selen.abstract import ActionAbstract
from selen import utils

class Inbox_archive_all(ActionAbstract):

	def apply(self):
		print(f'Firing Action: {self.__class__.__name__}...')
		driver = self.isp.driver

		# print('Start ActionChains...')
		actions = ActionChains(driver)
		# Go to inbox
		actions.send_keys('g').send_keys('i')
		time.sleep(2)

		# Scroll down.
		with utils.scroll_down(driver, 'div.customScrollBar.RKFl-TUsdXTE7ZZWxFGwX'):

			# choose msgs randomly
			"""
			let messages = Object.values($("div[role=checkbox]"))
			messages.pop(0) // to remove the 'select all' checkbox
			"""

			time.sleep(2)
			# Archive all selected messages.
			actions.send_keys('e').perform()

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