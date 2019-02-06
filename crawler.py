#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Chrome driver download url
# http://chromedriver.chromium.org/downloads


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import json
from urllib.request import Request
from urllib.request import urlopen
import concurrent.futures

# chrome dirver directory
CHROME_DIRVER = os.getcwd() + "/driver/chromedriver"
DOWNLOAD_PATH = "downloaded/"
# google image search url
GOOGLE_IMAGE_SEARCH_PREFIX = "https://www.google.com/search?tbm=isch&q="
# user agent
# https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
# to avoid Forbidden issue
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"

# search key words
SEARCH_KEY = "python lectures"
# search count
SEARCH_COUNT = 10
IMAGES_PATH = SEARCH_KEY.replace(" ", "_")

MAX_WORKERS = 5


def main():
    if not os.path.exists(DOWNLOAD_PATH + IMAGES_PATH):
        os.makedirs(DOWNLOAD_PATH + IMAGES_PATH)

    url = GOOGLE_IMAGE_SEARCH_PREFIX + SEARCH_KEY

    # set Chrome headless option
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Chrome browser
    with webdriver.Chrome(options=chrome_options, executable_path=CHROME_DIRVER) as driver:
        try:
            driver.get(url)
            images = driver.find_elements_by_class_name("rg_meta")
            print("Total images: {}".format(len(images)))
        except Exception as e:
            print("find_element_by_xpath error : {}".format(e))
            driver.quit()

        download_images(images)


def save_images(request, file_name):
    with urlopen(request) as raw:
        raw_image = raw.read()
        with open(DOWNLOAD_PATH + IMAGES_PATH + "/" + file_name, "wb") as file:
            print("Downloading {}".format(file_name))
            file.write(raw_image)


def download_images(images):
    headers = {}
    headers["User-Agent"] = USER_AGENT
    image_count = 0
    downloaded_images_count = 0

    for image in images:
        image_count += 1
        image_url = json.loads(image.get_attribute("innerHTML"))["ou"]
        image_title = json.loads(image.get_attribute("innerHTML"))["pt"]
        image_type = json.loads(image.get_attribute("innerHTML"))["ity"]
        if not image_type:
            image_type = "jpg"
        file_name = str(image_count) + "." + image_title + "." + image_type
        # print("Image url : {}".format(image_url))

        try:
            request = Request(image_url, headers=headers)

            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                executor.submit(save_images, request, file_name)
                downloaded_images_count += 1
        except Exception as e:
            print("Download failed: {}".format(e))

        if downloaded_images_count >= SEARCH_COUNT:
            break

    print("Total downloaded: {}/{}".format(downloaded_images_count, image_count))

if __name__ == "__main__":
    main()
