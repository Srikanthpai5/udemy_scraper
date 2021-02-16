from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import time

# --------------------------------------------------------------

driver = webdriver.Chrome("D:\\PyCharm_Files\\selenium\\chromedriver_win32\\chromedriver.exe")
delay = 15



def extract_text(soup_obj, tag, attribute_name, attribute_value):
    txt = soup_obj.find(tag, {attribute_name: attribute_value}).text.strip() if soup_obj.find(tag, {attribute_name: attribute_value}).text.strip() else ''
    return txt

rows = []


for page in range(1,12):
    page_url = f'https://www.udemy.com/courses/free/?lang=en&p={page}&sort=highest-rated'
    driver.get(page_url)
    time.sleep(5)

    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'course-list--container--3zXPS')))
    except TimeoutException:
        print('Loading exceeds delay time')
        # break
    else:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        course_list = soup.find('div', {'class': 'course-list--container--3zXPS'})

        courses = course_list.find_all('a', {'class' : "udlite-custom-focus-visible browse-course-card--link--3KIkQ"})
        # total_res = driver.find_element(By.CLASS_NAME,"udlite-heading-md filter-panel--item-count--2JGx3")
        #
        # print("----------------- FOUND :",total_res, " RESULTS !-----------------")

        for course in courses:
            course_url = '{}{}'.format("https://www.udemy.com",course['href'])
            course_title = course.select('div[class*="course-card--course-title"]')[0].text
            course_details = course.find_all('span', {'class':'course-card--row--1OMjg'})
            course_len = course_details[0].text
            number_of_lectures = course_details[1].text
            difficulty = course_details[2].text
            course_rating = extract_text(course, "span", 'data-purpose', 'rating-number')

            rows.append(
                [course_title, course_url, course_len, number_of_lectures, difficulty, course_rating]
                            )
columns = ['course_title', 'course_url', 'course_len', 'number_of_lectures', 'difficulty', 'course_rating']

df = pd.DataFrame(data=rows, columns=columns)
df.to_csv('Udemy.csv', index=False)

time.sleep(10)
driver.quit()

