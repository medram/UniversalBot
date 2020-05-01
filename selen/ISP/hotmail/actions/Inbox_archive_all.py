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
			# print('scrolling is done.')
			# select all msgs.
			utils.select_all_msgs(driver)
			# print('messages are selected')
			time.sleep(5)
			# print('timeout ends')
			# Archive all selected messages.
			actions = ActionChains(driver)
			actions.send_keys('e').perform()
			# print('Archive now')

			wait = WebDriverWait(driver, 15)
			undo_notification = (By.CSS_SELECTOR, 'div#notificationBarText div')
			try:
				if wait.until(EC.presence_of_element_located(undo_notification)) \
					and wait.until_not(EC.presence_of_element_located(undo_notification)):
					# print('Confirm')
					# wait to make sure the action is applied
					time.sleep(3)
			except TimeoutException:
				print(f'{self.__class__.__name__} not granted')