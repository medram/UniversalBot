import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


from selen.abstract import ActionAbstract
from selen import utils

class Spam_report_all_to_inbox(ActionAbstract):

	def apply(self):
		print(f'Firing Action: {self.__class__.__name__}...')
		driver = self.isp.driver

		# print('Start ActionChains...')
		# Go to Junk section
		driver.get('https://outlook.live.com/mail/junkemail')

		with utils.document_completed(driver, 20):
			# let javascript requests finish.
			time.sleep(5)

			# Scroll down.
			with utils.scroll_down(driver, 'div.customScrollBar.RKFl-TUsdXTE7ZZWxFGwX'):
				actions = ActionChains(driver)

				# select all msgs.
				utils.select_all_msgs(driver)
				time.sleep(5)

				# report all to inbox.
				try:
					not_junk_button = driver.find_elements_by_css_selector('button.ms-Button.T-xELtdXJl3uwSp_eaCQ4')[1]
					not_junk_button.click()
					# click to "Not junk" button.
					actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

					time.sleep(1)
					wait = WebDriverWait(driver, 15)
					undo_notification = (By.CSS_SELECTOR, 'div#notificationBarText div')
					if wait.until(EC.presence_of_element_located(undo_notification)) \
				 		and wait.until_not(EC.presence_of_element_located(undo_notification)):
						# print('Confirm')
						# wait to make sure the action is applied
						time.sleep(10)
				except TimeoutException:
					print(f'{self.__class__.__name__} not granted')
