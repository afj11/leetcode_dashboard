from flask import Flask
from forms import LoginForm
from flask import render_template, flash, redirect, url_for
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import itertools
from itertools import groupby
import pandas as pd
from collections import Counter
import operator
import pickle
from random import shuffle

load = False
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route("/",methods=['GET','POST'])

def home():
    form = LoginForm()
    if form.validate_on_submit():
        options = webdriver.ChromeOptions();
        options.add_argument('headless');
        browser = webdriver.Chrome(options = options)
        url = 'https://leetcode.com/accounts/login/'
        browser.get(url)
        time.sleep(10)
        a = browser.find_elements_by_class_name("input__2W4f")
        a[0].send_keys(str(form.username.data))
        a[1].send_keys(str(form.password.data))
        time.sleep(5)
        c = browser.find_elements_by_class_name("btn-content-container__214G")
        c[0].click()
        time.sleep(10)
        browser.get('https://leetcode.com/submissions/#/1')
        time.sleep(5)
        innerHTML = browser.execute_script("return document.body.innerHTML")
        page_data = BeautifulSoup(innerHTML, features = "html.parser")
        table_data = page_data.find_all("tbody")

        if(table_data == []):
            l = 'wrong password or username'
            return render_template('login2.html', form=form, l = l)
        all = []

        count_var = 2
        while page_data.find_all("div", class_ = "placeholder-text") == []:
            table_info = []
            for data in table_data:
                td = data.find_all("td")
                values = []

                for data in td:
                    if(data.find_all("a") != []):
                        table_info.append(data.find_all("a")[0].get("href"))
                    table_info.append(data.text)
            table_info = [x.replace('\xa0',' ')  for x in table_info]
            table_info = [x.strip() for x in table_info]
            table_info = [table_info[x:x+6] for x in range(0, len(table_info),6)]
            all.append(table_info)
            url = 'https://leetcode.com/submissions/#/' + str(count_var)
            browser.get(url)
            time.sleep(6)
            innerHTML = browser.execute_script("return document.body.innerHTML")
            page_data = BeautifulSoup(innerHTML, features = "html.parser")
            table_data = page_data.find_all("tbody")
            count_var += 1

        submissions = all

        submissions = list(itertools.chain.from_iterable(submissions))

        print(submissions)
        names2 = [x[1] for x in submissions]
        print(names2)

        right = []
        wrong = []

        for data in submissions:
            if data[3] == 'Accepted':
                right.append(data[1])
            else:
                wrong.append(data[1])

        with open('all_info.pkl', 'rb') as f:
           question_basic = pickle.load(f)

        with open('full_q_data.pkl', 'rb') as f:
             question_data = pickle.load(f)

        names = [x[0] for x in question_basic]

        company = set()
        for data in question_data:
            for comp in data[1]:
                company.add(comp[0])

        tags = set()
        for data in question_data:
            for t in data[2]:
                for data in t:
                    tags.add(t)

        company_list = []
        for data in question_data:
            temp = []
            for val in data[1]:
                temp.append(val[0])
            company_list.append(temp)

        data = {'likes': [int(question_data[i][0][0]) for i in range(len(question_data))],
             'dislikes': [int(question_data[i][0][1]) for i in range(len(question_data))],
              'article_link' : [question_basic[i][1] for i in range(len(question_basic))],
              'accept_percent' : [question_basic[i][2] for i in range(len(question_basic))],
             'difficultly' : [question_basic[i][3] for i in range(len(question_basic))],
             'freq_value' : [question_basic[i][4] for i in range(len(question_basic))],
              'problem_link' : [question_basic[i][5] for i in range(len(question_basic))],
              'tag_list' : [question_data[i][2] for i in range(len(question_data))],
              'company' : company_list
}

        for val in company:
            data[val] = 0

        for val in tags:
            data[val] = 0

        df = pd.DataFrame(data, index = names)
        pd.options.mode.chained_assignment = None

        for count, val in enumerate(question_data):
            for val1 in val[1]:
                df[val1[0]][names[count]] = val1[1]

        for count, val in enumerate(question_data):
            for val1 in val[2]:
                df[val1][names[count]] = 1

        tag_right_count = []
        tag_wrong_count = []

        diff_right_count = []
        diff_wrong_count = []

        comp_right_count = []
        comp_wrong_count = []

        for data in right:
            comp_right_count.append(df['company'][data])

        for data in wrong:
            comp_wrong_count.append(df['company'][data])

        for data in right:
            diff_right_count.append(df['difficultly'][data])

        for data in wrong:
            diff_wrong_count.append(df['difficultly'][data])

        for data in right:
            tag_right_count.append(df['tag_list'][data])

        for data in wrong:
            tag_wrong_count.append(df['tag_list'][data])

        comp_right_count = list(itertools.chain.from_iterable(comp_right_count))
        comp_wrong_count = list(itertools.chain.from_iterable(comp_wrong_count))

        tag_right_count = list(itertools.chain.from_iterable(tag_right_count))
        tag_wrong_count = list(itertools.chain.from_iterable(tag_wrong_count))

        comp_right_freq = Counter(comp_right_count)
        comp_wrong_freq = Counter(comp_wrong_count)

        del_list = []

        for data in comp_right_freq:
            if (comp_right_freq[data] + comp_wrong_freq[data]) < 10:
                del_list.append(data)

        for data in del_list:
            del comp_right_freq[data]

        diff_right_freq = Counter(diff_right_count)
        diff_wrong_freq = Counter(diff_wrong_count)

        tag_right_freq = Counter(tag_right_count)
        tag_wrong_freq = Counter(tag_wrong_count)

        comp_ratio = {}
        for data in comp_right_freq:
            comp_ratio[data] = round((comp_right_freq[data] / ((comp_right_freq[data] + comp_wrong_freq[data])) * 100), 2)

        diff_ratio = {}
        for data in diff_right_freq:
            diff_ratio[data] = round((diff_right_freq[data] / ((diff_right_freq[data] + diff_wrong_freq[data])) * 100), 2)

        tag_ratio = {}
        for data in tag_right_freq:
            tag_ratio[data] = round((tag_right_freq[data] / ((tag_right_freq[data] + tag_wrong_freq[data])) * 100), 2)

        def ratio_string(convert, right, wrong):
            ret = []
            for data in convert:
                ret.append([data[0], str(data[1]) + "%", str(right[data[0]]) + "/" +
                str((right[data[0]] + wrong[data[0]]))])
            return ret

        comp_ratio = sorted(comp_ratio.items(), key=operator.itemgetter(1), reverse = True)

        tag_ratio = sorted(tag_ratio.items(), key=operator.itemgetter(1), reverse = True)

        diff_ratio = sorted(diff_ratio.items(), key=operator.itemgetter(1), reverse = True)

        diff_ratio_str = ratio_string(diff_ratio, diff_right_freq, diff_wrong_freq)

        tag_ratio_str = ratio_string(tag_ratio, tag_right_freq, tag_wrong_freq)

        comp_ratio_str = ratio_string(comp_ratio, comp_right_freq, comp_wrong_freq)

        tag = []
        for data in tag_ratio_str:
            tag.append(data)

        diff = []
        for data in diff_ratio_str:
            diff.append(data)

        company_html = []
        for data in comp_ratio_str:
            company_html.append(data)

        new_questions = tag_ratio[::-1]

        new_questions = [x for x in new_questions if int(x[1]) < 50]

        questions = []
        for i in range(int(len(new_questions))):
            try:
                questions.append(df[df[new_questions[i][0]] > 0])
            except:
                pass

        for data in questions:
            data.sort_values(by = ['freq_value'], inplace = True, ascending = False)

        suggestions = []

        for data in questions:
            count = 0
            for val in enumerate(data.index.values):
                if count == 10:
                    break
                print("get here???")
                if(val[1] not in names2):
                    print(val, "here??")
                    suggestions.append([val[1], df['problem_link'][val[1]]])
                    count+=1

        shuffle(suggestions)

        js_labels = []
        js_values = []

        for data in tag:
            js_labels.append(data[0] + " " + data[2])
            js_values.append(data[2])

        js_val_c = []
        for data in js_values:
            a = data.split("/")
            for count, val in enumerate(a):
                a[count] = int(val)
            js_val_c.append(a)

        js_right = []
        js_wrong = []
        for data in js_val_c:
            js_right.append(data[0])
            js_wrong.append(data[1]-data[0])

        js_labels1 = []
        js_values1 = []

        for data in diff:
            js_labels1.append(data[0] + " " + data[2])
            js_values1.append(data[2])

        js_val_c1 = []
        for data in js_values1:
            a = data.split("/")
            for count, val in enumerate(a):
                a[count] = int(val)
            js_val_c1.append(a)

        js_right1 = []
        js_wrong1 = []
        for data in js_val_c1:
            js_right1.append(data[0])
            js_wrong1.append(data[1]-data[0])

        js_labels2 = []
        js_values2 = []

        for data in company_html:
            js_labels2.append(data[0] + " " + data[2])
            js_values2.append(data[2])


        js_val_c2 = []
        for data in js_values2:
            a = data.split("/")
            for count, val in enumerate(a):
                a[count] = int(val)
            js_val_c2.append(a)

        js_right2 = []
        js_wrong2 = []
        for data in js_val_c2:
            js_right2.append(data[0])
            js_wrong2.append(data[1]-data[0])

        return render_template('login.html', form=form, tag=tag, diff = diff, company_html = company_html, suggestions = suggestions,
        labels = js_labels,right = js_right, wrong = js_wrong, labels1 = js_labels1, right1 = js_right1, wrong1 = js_wrong1,
        labels2 = js_labels2, right2 = js_right2, wrong2 = js_wrong2, num = len(suggestions))
    l = ''
    global load
    if(load):
        l = 'Invalid Data'
    load = True
    return render_template('login2.html', form=form, l = l)

if __name__ == "__main__":
    app.run(debug=True)
