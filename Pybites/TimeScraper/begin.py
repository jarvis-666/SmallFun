from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time

driver = webdriver.Firefox(executable_path=r"C:\Users\Vin\Downloads\geckodriver-v0.27.0-win64\geckodriver")
driver.get(r"https://www.udemy.com/course/complete-python-bootcamp/")
time.sleep(20)
driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div/div/div[2]/button[2]').click()
time.sleep(20)
script = "window.scrollBy(0, 1300);"
driver.execute_script(script)
time.sleep(10)
driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[4]/div[5]/div/div/div/div/button').click()
res = driver.page_source
# print(res)
if res is not None:
    print("Received the data successfully")
    try:
        soup = BeautifulSoup(res, 'html.parser')
        # print(soup.prettify())
        # print(soup.find_all('span', class_="section--hidden-on-mobile--171Q9 section--item-content-summary--126oS"))
        list_of_spans = soup.find_all('span', class_="section--hidden-on-mobile--171Q9 section--item-content-summary--126oS")
        list_of_supposed_durations = [i.contents for i in list_of_spans]
        list_of_supposed_durations = [i[0] for i in list_of_supposed_durations]
        # print(list_of_supposed_durations)
        list_minutes = []
        list_seconds = []
        for i in list_of_supposed_durations:
            if not re.search('question', i):
                list_minutes.append(int(i.split(':')[0]))
                list_seconds.append(int(i.split(':')[1]))
        minutes = sum(list_minutes)
        seconds = sum(list_seconds)
        hours, minutes = divmod(minutes, 60)
        secmins, seconds = divmod(seconds, 60)
        hours_new, minutes = divmod(minutes + secmins, 60)
        hours = hours + hours_new
        print(f"Course Content has the following duration\n{hours} hours, {minutes} minutes, {seconds} seconds")
    except Exception as err:
        print(f"Failed with the following exception: {err}")
        print("Exiting Now")
else:
    print("Failed to retrieve the data, try another URL")
