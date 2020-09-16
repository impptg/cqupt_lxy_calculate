# create by pptg 2020/9/7
import pandas as pd
import numpy as np
import os
from pp_support import *
from pp_network import *

# 尘封的1.0离线获取学分函数，人工太费时间了，改成了爬取
# time_str = '2019'  # 2019
# class_list = []
# pp_getAll(time_str, class_list)  # 根据学期 和 班级列表 合并文件数据到一个文件里

for fn in os.listdir('./input'):
    print(fn)
    df = pd.read_excel('./input/'+fn) # 读数据
    data_np = np.array(df)  # 将df转换成数组 将用于计算
    grader = pp_grader(df.columns)  # 爬取课程学分
    a = pp_data(data_np) # 处理数据

    res = np.zeros((a.shape[0], 3))  # 用于记录结果: 加权总成绩 、 权和 、 加权平均
    for i in range(a.shape[0]):
        all = 0  # 加权总成绩
        all_id = 0  # 权和
        for j in range(a.shape[1]):
            if (a[i, j] == -2):  # 未选的不算
                continue
            elif (a[i, j] == -1): # 已经修改了，补考算补考后的分，不影响
                all_id += grader[j]  # 补考了，总成绩不加，总权加
            else:  # 可算来个正常人了
                # print(a[i,j])
                # print(grader[j])
                try:
                    ag = a[i, j] * grader[j]  # 成绩 * 权
                except:
                    continue
                else:
                    all += ag
                    all_id += grader[j]
        # 一个人的统计结束
        if(all_id < 0.1):   # 判断浮点0，这人一个课没选
            per = 0
        else:   #正常人
            per = all / all_id  # 计算平均学分成绩
        # 记录
        res[i, 0] = all
        res[i, 1] = all_id
        res[i, 2] = per

    # 结果添加到含姓名学号的data的末尾
    new_list = np.append(data_np, res, axis=1)
    # 将所有人根据加权平均排列 new_data即为所需
    n = np.argsort(new_list[:, -1])
    new_data = new_list[n[::-1]]

    # 保存文件
    new_col = df.columns.tolist() + ["总成绩","总学分","平均学分成绩"]
    new_df = pd.DataFrame(new_data, index=df.index,
                       columns=new_col)
    new_df.to_excel('./output/result'+fn+'x')
