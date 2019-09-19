# Leetcode Dashboard
Leetcode is a great website for practicing interview questions, but their statistics are lacking, and finding good questions to work on can also be a challenge.  This project scapes submission data from a user's account and generates detailed statistics and recommends questions tailored to their needs.
# How to install
When using flask, it is good to use a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/), so after setting up a virtual environment, pip install requirements.txt.  Then download a [chrome driver](https://chromedriver.chromium.org/downloads) to run the headless browser.  This [link](https://help.zenplanner.com/hc/en-us/articles/204253654-How-to-Find-Your-Internet-Browser-Version-Number-Google-Chrome) describes how to find the current chrome version and thus which version of the driver you should install.
# How to use it
Once you get it running, you can open the flask page in your web browser and enter your leetcode password and username (Don't worry, this is all local to your machine).  A browser will open in the background, sign into your account, and start scapining your submission data.  The flask page will then update to include statistics on your submissions and a graphical display of that data.
# What to expect when running
The following screenshots show the login page followed by the expected program output.
![](https://github.com/afj11/leetcode_dashboard/blob/master/home.PNG)
![](https://github.com/afj11/leetcode_dashboard/blob/master/question_type.PNG)
![](https://github.com/afj11/leetcode_dashboard/blob/master/question_diff_and_company.PNG)
![](https://github.com/afj11/leetcode_dashboard/blob/master/question_sugg.PNG)
![](https://github.com/afj11/leetcode_dashboard/blob/master/select_q.PNG)
![](https://github.com/afj11/leetcode_dashboard/blob/master/q_graph_1.PNG)
![](https://github.com/afj11/leetcode_dashboard/blob/master/q_graph_2.PNG)
![](https://github.com/afj11/leetcode_dashboard/blob/master/q_graph_3.PNG)
