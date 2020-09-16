# create by pptg 2020/9/16
import requests
import pandas as pd
import numpy as np

# 需要内网，自动爬取成绩
def pp_grader(col):
    url1 = 'http://cc.cqupt.edu.cn/getCourseHomePageMsg?kcbh='
    url2 = '&unifyCode=1'
    grader = np.zeros(col.size)
    for i in range(2, col.size):
        str = col[i]
        url = url1 + str[0:8] + url2
        req = requests.get(url=url)
        req.encoding = 'UTF-8'
        c = req.text
        ins = c.find('xf')
        grade = c[ins + 5:ins + 8]
        print(str + ':' + grade)
        try:
            g = float(grade)
        except:
            grader[i-2] = input(str + ': 课程已被删除或更换名称，请手动输入学分 + 回车')
        else:
            grader[i-2] = g

    return grader