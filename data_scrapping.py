from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import io
from PIL import Image
import time

# install Chrome webdriver then put file path here
PATH = 'D:\\ml_project\\passio_cake_classification\\chromedriver.exe'

# promt user to get search input
search_term = input('whatya wanna search: ')

wd = webdriver.Chrome(PATH)

# paste search_url here
# search_url = 'https://www.google.com/search?q=bun+bo+hue&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj2wsTw4932AhVS1GEKHdzBCXAQ_AUoAXoECAIQAw&biw=1474&bih=794&dpr=1.25'

#go google search and look for images
wd.get('https://images.google.com')
m = wd.find_element_by_name("q") #identify search box
m.send_keys(search_term)
m.send_keys(Keys.ENTER)
search_url = wd.current_url

#get image urls from google search
def get_images_from_google(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

	url = search_url
	wd.get(url)

	image_urls = set()
	skips = 0

	while len(image_urls) + skips < max_images:
		scroll_down(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        # try to click every thumbnail to get to the actual image link
		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					print(f"Found {len(image_urls)}")

	return image_urls

#
urls = get_images_from_google(wd, delay=1, max_images=100)


#download images from image_urls
def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name
        with open(file_path, "wb") as f:
            image.save(f, "JPEG")
        print("download success")
    except Exception as e:
        print('FAILED',e)


for i, url in enumerate(urls):
	download_image("images/ ", url, search_term + str(i) + ".jpg")

wd.quit()
