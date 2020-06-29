import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selen.abstract import ActionAbstract
from selen import utils, exceptions


class Inbox_archive_all(ActionAbstract):

	def apply(self):
		print(f'Firing Action: {self.__class__.__name__}...')
		driver = self.isp.driver

		driver.implicitly_wait(2)
		driver.get('https://mail.google.com/mail/u/0/#inbox')
		# print(driver.title)
		time.sleep(1)
		driver.implicitly_wait(5)

		try:
			WebDriverWait(driver, 2).until(
				EC.presence_of_element_located((By.CSS_SELECTOR, 'tr.zA')))
		except Exception as e:
			driver.quit()
			raise exceptions.EmptyInbox()
		else:
			check_all = driver.find_element_by_css_selector('span.T-Jo')
			# driver.implicitly_wait(5)
			# check_all_emails.send_keys(Keys.RETURN)
			# ActionChains(driver).send_keys(Keys.ENTER)
			ActionChains(driver).click(check_all).perform()
			# div.ya > span[role=link]
			driver.implicitly_wait(5)
			time.sleep(3)
			try:
				check_all_emails = driver.find_element_by_css_selector(
					'div.ya > span[role=link]')
			except NoSuchElementException:
				# delete emails less than max per page
				ActionChains(driver).send_keys('e').perform()
			else:
				# delete all emails on primary section.
				ActionChains(driver).click(check_all_emails).pause(1).send_keys(
					'e').send_keys(Keys.ENTER).perform()

			try:
				time.sleep(1)
				wait = WebDriverWait(driver, 60)
				element = (By.CSS_SELECTOR, 'div.vh > span.aT')
				if wait.until(EC.presence_of_element_located(element)) \
				   and wait.until_not(EC.presence_of_element_located(element)):
					time.sleep(3)
			except TimeoutException as e:
				print(f'{self.__class__.__name__} not granted')