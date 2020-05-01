import contextlib

from selenium.webdriver.support.events import AbstractEventListener
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class MyListeners(AbstractEventListener):
	def before_close(self, driver):
		print('fire before close function.')

	def before_quit(self, driver):
		print('fire before quit function.')
		# with open('cookies/test.cks', 'w') as f:
		# 	json.dump(driver.get_cookies(), f, indent=2)
		# shutil.rmtree(profile_path, ignore_errors=True)
		# shutil.copytree(driver.firefox_profile.path, profile_path)


# EC
def doc_complete(driver):
	return driver.execute_script("return document.readyState") == 'complete'

# EC
class is_scroll_down:
	def __init__(self, css_selector):
		self.css_selector = css_selector

	def __call__(self, driver):
		# print('scrolling...')
		return driver.execute_script("""
			let element = document.querySelector('%s')
			if ((element.scrollTop + element.clientHeight) < element.scrollHeight)
			{
				console.log('Scrolling...')
				element.scrollTo(0, element.scrollHeight)
				return false
			}
			// the scroll has reached the bottom.
			return true
			""" % self.css_selector)


@contextlib.contextmanager
def document_completed(driver, timeout=10):
	WebDriverWait(driver, timeout, ignored_exceptions=(TimeoutException,)).until(doc_complete)
	yield


@contextlib.contextmanager
def scroll_down(driver, css_selector, timeout=60, poll_frequency=2):
	if css_selector:
		WebDriverWait(driver, timeout, poll_frequency=poll_frequency, ignored_exceptions=(TimeoutException,)).until(is_scroll_down(css_selector))
	yield



@contextlib.contextmanager
def screen_is_loaded(driver, timeout=60):
	# print('is screen loaded ?!')
	wait = WebDriverWait(driver, timeout=timeout, ignored_exceptions=(TimeoutException,))
	yield wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#loadingScreen')))


def select_all_msgs(driver):
	driver.execute_script("""
		let messages = Object.values(document.querySelectorAll('div[role=checkbox]'))
		
		messages = messages.slice(1)

		messages.map((msg, i) => {
			msg.click()
		})
	""")
