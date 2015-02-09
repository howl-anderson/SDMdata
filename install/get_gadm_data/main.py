from selenium import webdriver
from selenium.webdriver.support.ui import Select

url_list = []
for index in range(0, 253):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("permissions.default.image", 2)
    profile.set_preference("permissions.default.script", 2)
    profile.set_preference("permissions.default.stylesheet", 2)
    profile.set_preference("permissions.default.subdocument", 2)

    # profile.native_events_enabled = True
    driver = webdriver.Firefox(profile)
    driver.implicitly_wait(30)
    base_url = "http://www.gadm.org/"

    driver.get(base_url + "country")
    Select(driver.find_element_by_name("cnt")).select_by_index(index)
    driver.find_element_by_name("OK").click()
    url = driver.find_element_by_css_selector("div.content a").get_attribute("href")
    driver.quit()
    url_list.append(url)

import subprocess

for url in url_list:
    subprocess.Popen("wget " + url, shell=True)