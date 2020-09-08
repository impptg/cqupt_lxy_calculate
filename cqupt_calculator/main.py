# create by pptg 2020/9/7
import pandas as pd
import numpy as np
from pp_support import *

# 1.数据合并
time_str = '2019'  # 2019学期
# 因为要兼容 macos 和 win 所以这里就手动填一下班级号，不写自动化了,反正也没几个班
class_list = ['11021701',
              '11021702',
              '11021703']

# pp_getAll(time_str, class_list)  # 根据学期 和 班级列表 合并文件数据到一个文件里

# 2.使用任意软件打开 'time_str + all.xlsx'例如2019all.xlsx
# 将你想计算的科目名字末尾添加 _和学分 例如 ： A123123数学分析  -> A123123数学分析_5.5
# 稍后的脚本会认为添加了 _学分 的科目为需要计算的科目，并会自动弃掉其他科目
# 添加之后保存并运行后续所有代码即可
# 谨慎注意这一步骤，建议将生成的例如 2019all.xlsx改名并将下面读取改成他的新名字
# 因为如果重新运行会把你辛苦填写的学分变没
# 或者将上面 pp_getAll(time_str, class_list) 注销吊也可以,因为系统这里就不写自动检测了

# 3.数据预处理
df = pd.read_excel(time_str + 'all.xlsx')
classes = df.columns  # 获得数据的列名称 (学号，姓名 ...)
grader = np.zeros(classes.size)  # 创建一个计入计算学分记录数组(也就是xlsx中课程名称加 _学分的部分 例如 数分: _5.5
grader_id = 0  # 用于管理计入计算学分记录数组的下标
geter = np.zeros(classes.size, dtype=int)  # 用于获取计入计算的列的标签(例如 记录 数分科目在第几列

print('需要计算的科目有:')
for i in range(0, classes.size):
    str = classes[i]
    if (pp_number(str[-1]) and str[-2] == '_'):  # 也就是寻找 _学分
        grader[grader_id] = float(str[-1])
        geter[grader_id] = int(i)
        grader_id = grader_id + 1
        print(classes[i])  # 输出计算的科目名 方便检查错误
    elif(pp_number(str[-3:]) and str[-4] == '_'):    # 学分为 _x.y情况
        grader[grader_id] = float(str[-3:])
        geter[grader_id] = int(i)
        grader_id = grader_id + 1
        print(classes[i])  # 输出计算的科目名 方便检查错误
    elif(pp_number(str[-2:]) and str[-3] == '_'):    # 学分为 _.y情况
        grader[grader_id] = float(str[-2:])
        geter[grader_id] = int(i)
        grader_id = grader_id + 1
        print(classes[i])  # 输出计算的科目名 方便检查错误

data_np = np.array(df)  # 将df转换成数组 将用于计算
data = data_np[:, np.append([1, 2], geter[0:grader_id])]  # 从原数组里取出学号、姓名和需要计算的科目

# 先行后列 data[1,2] : 第一个人的第二门成绩
# 这里清洗的数据已经是全部是成绩的数据了
# 这里将 正常的成绩 保留
# 将 未选课 的成绩 变成 -2
# 将 含有实验课的 正常成绩去掉实验:90(79) -> 90 未选课的 (0) -> 0 , () -> 0    (这里我不确定未选课的形式，可以问一下同学)
# 将 补考的(特点是含有 ])变成-1

for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        str = data[i, j]
        if (pp_number(str)):  # 如果这个单元格的字符能被转换为数值
            if (np.isnan(str)):  # 如果这个数值是 nan 也就是这个人没有选这门课
                data[i, j] = -2
            else:
                continue  # 正常成绩不变
        elif (']' in str):
            data[i, j] = -1  # 补考为-1
        elif (')' in str):  # 实验课未补考的
            str_new = pp_clear(str)  # 清楚括号
            if (pp_number(str_new)):
                data[i, j] = float(str_new)  # 正常成绩
            else:
                data[i, j] = -2  # 未补考的 也 非正常成绩 -> 未选

a = data[:, 2:]  # 取出data里成绩部分(去掉学号、姓名)
res = np.zeros((a.shape[0], 3))  # 用于记录结果: 加权总成绩 、 权和 、 加权平均
for i in range(a.shape[0]):
    all = 0  # 加权总成绩
    all_id = 0  # 权和
    for j in range(a.shape[1]):
        if (a[i, j] == -2):  # 未选的不算
            continue
        elif (a[i, j] == -1):
            all_id += grader[j]  # 补考了，总成绩不加，总权加
        else:  # 可算来个正常人了
            all += a[i, j] * grader[j]  # 成绩 * 权
            all_id += grader[j] # 权
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
new_col = df.columns.tolist() + ["总成绩","权","平均成绩"]
new_df = pd.DataFrame(new_data, index=df.index,
                   columns=new_col)
new_df.to_excel(time_str+'result.xlsx') # 记得更换文件名称或者移出目录，否则下次运行会替换掉
