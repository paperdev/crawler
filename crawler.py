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

# chrome dirver directory
CHROME_DIRVER = os.getcwd() + "/driver/chromedriver"
DOWNLOAD_PATH = "downloaded/"
# google image search url
GOOGLE_IMAGE_SEARCH_PREFIX = "https://www.google.com/search?tbm=isch&q="
# user agent
# https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
# to avoid Forbidden issue
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"


def main():
    # search key words
    search_key = "python lectures"
    # search count
    search_count = 3
    images_path = search_key.replace(" ", "_")

    if not os.path.exists(DOWNLOAD_PATH + images_path):
        os.makedirs(DOWNLOAD_PATH + images_path)

    url = GOOGLE_IMAGE_SEARCH_PREFIX + search_key

    # set Chrome headless option
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Chrome browser
    driver = webdriver.Chrome(options=chrome_options, executable_path=CHROME_DIRVER)
    driver.get(url)

    headers = {}
    headers["User-Agent"] = USER_AGENT
    extensions = {"jpg", "jpeg", "png", "gif"}
    image_count = 0
    downloaded_images_count = 0

    try:
        images = driver.find_elements_by_class_name("rg_meta")
        print("Total images: {}".format(len(images)))
    except Exception as e:
        print("find_element_by_xpath error : {}".format(e))
        driver.quit()

    for image in images:
        image_count += 1
        image_url = json.loads(image.get_attribute("innerHTML"))["ou"]
        image_type = json.loads(image.get_attribute("innerHTML"))["ity"]
        image_title = json.loads(image.get_attribute("innerHTML"))["pt"]
        print("Downloading from {}".format(image_url))
        try:
            if image_type not in extensions:
                continue
            request = Request(image_url, headers=headers)
            raw_image = urlopen(request).read()
            file_name = str(downloaded_images_count) + "." + image_title + "." + image_type
            file = open(DOWNLOAD_PATH + images_path + "/" + file_name, "wb")
            file.write(raw_image)
            file.close()
            downloaded_images_count += 1
        except Exception as e:
            print("Download failed: {}".format(e))
        finally:
            print("Download finished.")
        if downloaded_images_count >= search_count:
            break

    print("Total downloaded: {}/{}".format(downloaded_images_count, image_count))
    driver.quit()

if __name__ == "__main__":
    main()
