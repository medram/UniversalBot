import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selen.abstract import ActionAbstract
from selen import utils


class Inbox_open_messages(ActionAbstract):

	def apply(self):
		print(f'Firing Action: {self.__class__.__name__}...')
		driver = self.isp.driver

		# print('Start ActionChains...')
		actions = ActionChains(driver)
		# Go to inbox
		actions.send_keys('g').send_keys('i')
		time.sleep(2)

		# Scroll down.
		with utils.scroll_down(driver, 'div.customScrollBar.RKFl-TUsdXTE7ZZWxFGwX', poll_frequency=3):
			time.sleep(1)
			# select all msgs.
			msgs = driver.find_elements_by_css_selector('div._1xP-XmXM1GGHpRKCCeOKjP') 
			
			for i, msg in enumerate(msgs, 1):
				# open just 60 messages.
				if i > 60:
					break
				msg.click()
				# print(msg)
				try:
					wait = WebDriverWait(driver, 20)
					wait.until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.ms-Spinner')))
					# print('watch time.')
					time.sleep(random.uniform(1, 3))
				except TimeoutException:
					pass