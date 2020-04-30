import contextlib

from selenium.webdriver.support.events import AbstractEventListener
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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

	def __call_(self, driver):
		return driver.execute_script("""
			let element = document.querySelector(%s)
			if (element.scrollTop < element.scrollHeight)
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
	WebDriverWait(driver, timeout).until(doc_complete)
	yield


@contextlib.contextmanager
def scroll_down(driver, css_selector, timeout=120):
	if css_selector:
		WebDriverWait(driver, timeout, poll_frequency=1).until(is_scroll_down(css_selector))
	yield


# r = driver.execute_script("""
# 		let element = document.querySelector('div.customScrollBar.RKFl-TUsdXTE7ZZWxFGwX')
		
# 		let interval = setInterval(function(){
# 			if (element.scrollTop < element.scrollHeight)
# 			{
# 				console.log('Scrolling...')
# 				element.scrollTo(0, element.scrollHeight)
# 			}
# 			else
# 			{
# 				clearInterval(interval)
# 			}
# 		}, 500)

# 		return 'DONE'
# 	""")
# print(r)