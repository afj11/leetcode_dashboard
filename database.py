from flask import Flask
from forms import LoginForm
from flask import render_template, flash, redirect, url_for
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import pickle

options = webdriver.ChromeOptions();
options.add_argument('headless');
browser = webdriver.Chrome(options = options)
url = 'https://leetcode.com/accounts/login/'
browser.get(url)
time.sleep(15)
a = browser.find_elements_by_class_name("input__2W4f")
a[0].send_keys('username') # leetcode username
a[1].send_keys("password") #leetcode password
time.sleep(5)
c = browser.find_elements_by_class_name("btn-content-container__214G")
c[0].click()
time.sleep(10)
##browser.get('https://leetcode.com/problemset/all/?status=Solved')
browser.find_element_by_xpath("//select[@class='form-control']/option[text()='all']").click()
time.sleep(8)
innerHTML = browser.execute_script("return document.body.innerHTML")
problems_html = BeautifulSoup(innerHTML, features = "html.parser")
table_data = problems_html.find_all("tbody", class_ = "reactable-data")

info = []

for data in table_data:
    a = data.find_all("a")
    tr = data.find_all("tr")
    for data in tr:
        td = data.find_all("td")
        problem_data = []
        for data in td:
            problem_data.append(data)
        problem_data= problem_data[2:7]
        problem_data.append(problem_data[0].find_all("a")[0].get("href"))
        problem_data[0] = problem_data[0].text.strip()

        test = problem_data[1].find_all("a")
        if test:
            problem_data[1] = test[0].get("href")
        else:
            problem_data[1] = test
        problem_data[2] = problem_data[2].text
        problem_data[3] = problem_data[3].text
        problem_data[4] = problem_data[4]['value']
        info.append(problem_data)



with open('all_info.pkl', 'wb') as f:
    pickle.dump(info, f)

num = len(info)
all = []
cc = 1

error_count = 0
for data in info:
    while True:
        try:
            main = []
            browser.get('https://leetcode.com' + str(data[-1]))
            time.sleep(9)
            innerHTML = browser.execute_script("return document.body.innerHTML")
            page_data = BeautifulSoup(innerHTML, features = "html.parser")
            likes = page_data.find_all("button", class_ = "btn__r7r7 css-1rdgofi")


            like_dislike = []
            for data in likes:
                span = data.find_all("span")[0].text
                like_dislike.append(span)
            like_dislike = like_dislike[0:2]
            main.append(like_dislike)
            innerHTML = browser.execute_script("return document.body.innerHTML")
            page_data = BeautifulSoup(innerHTML, features = "html.parser")
            company = page_data.find_all("div", class_ = "company-tag-wrapper__1rBy")


            freq = []
            for data in company:
               a = data.find_all("a")
               for data in a:
                   x = data.get("href")
                   a = data.text.split("|")
                   freq.append(a)

            main.append(freq)

            topic = []

            related_topics = page_data.find_all("div", class_ = "css-1hky5w4")
            for data in related_topics:
               a = data.find_all("a", class_ = "topic-tag__1jni")
               for data in a:
                    topic.append(data.text)

            main.append(topic)
            all.append(main)
            cc+=1
            break
        except:
            time.sleep(5)
            pass

with open('full_q_data11.pkl', 'wb') as f:
    pickle.dump(all, f)
