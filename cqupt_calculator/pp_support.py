import re
import pandas as pd
import numpy as np

# 判断一个字符串是否能完全转化为数字
def pp_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

# 清楚字符串中的括号中间的内容 '80(90)' -> '80'
# 用于一些有实验课的课程
def pp_clear(str):
    str_new = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", str)
    return str_new

def pp_clear2(str):
    str_new = re.findall(r'[：](.*?)[]]', str)
    return str_new[0]


# 根据学期 和 班级 返回文件名
def pp_fn(time_str,a,class_str):
    fn = time_str + a + class_str + '.xlsx'
    return fn

# 根据学期 和 班级 合并所有文件
def pp_getAll(time_str,class_list):
    fn1 = pp_fn(time_str,'1', class_list[0])
    fn2 = pp_fn(time_str,'2',class_list[0])
    df1 = pd.read_excel(fn1, sheet_name=0, header=0)
    df1['class'] = class_list[0]
    df2 = pd.read_excel(fn2, sheet_name=0, header=0)
    df2['class'] = class_list[0]
    dff1 = pd.merge(df1,df2,how='outer',left_on='姓名',right_on='姓名')
    for i in range(1, class_list.__len__()):
        fn1 = pp_fn(time_str, '1', class_list[i])
        fn2 = pp_fn(time_str, '2', class_list[i])
        df1 = pd.read_excel(fn1,sheet_name=0,header=0)
        df2 = pd.read_excel(fn2, sheet_name=0, header=0)
        df1['class'] = class_list[i]
        df2['class'] = class_list[i]
        dff2 = pd.merge(df1,df2,how='outer',left_on='姓名',right_on='姓名')
        dff1 = dff1.append(dff2)

    dff1.to_excel(time_str+'all.xlsx')

# 根据本地文件进行读取学分
def pp_grader_local(classes):
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
        elif (pp_number(str[-3:]) and str[-4] == '_'):  # 学分为 _x.y情况
            grader[grader_id] = float(str[-3:])
            geter[grader_id] = int(i)
            grader_id = grader_id + 1
            print(classes[i])  # 输出计算的科目名 方便检查错误
        elif (pp_number(str[-2:]) and str[-3] == '_'):  # 学分为 _.y情况
            grader[grader_id] = float(str[-2:])
            geter[grader_id] = int(i)
            grader_id = grader_id + 1
            print(classes[i])  # 输出计算的科目名 方便检查错误

    for i in range(grader.shape[0]):
        if (grader[i] - round(grader[i])) < 0.3:
            grader[i] = round(grader[i])
    return grader

# 先行后列 data[1,2] : 第一个人的第二门成绩
# 这里清洗的数据已经是全部是成绩的数据了
# 这里将 正常的成绩 保留
# 将 未选课 的成绩 变成 -2
# 将 含有实验课的 正常成绩去掉实验:90(79) -> 90 未选课的 (0) -> 0 , () -> 0    (这里我不确定未选课的形式，可以问一下同学)
# 将 补考的(特点是含有 ])变成 提取[]内的成绩
def pp_data(data):
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            str = data[i, j]
            if (pp_number(str)):  # 如果这个单元格的字符能被转换为数值
                if (np.isnan(str)):  # 如果这个数值是 nan 也就是这个人没有选这门课
                    data[i, j] = -2
                else:
                    continue  # 正常成绩不变
            elif (']' in str):
                print(str)
                str_new = pp_clear2(str)
                data[i, j] = float(str_new)  # 补考
            elif (')' in str):  # 实验课未补考的
                str_new = pp_clear(str)  # 清楚括号
                if (pp_number(str_new)):
                    data[i, j] = float(str_new)  # 正常成绩
                else:
                    data[i, j] = -2  # 未补考的 也 非正常成绩 -> 未选

    return data[:, 2:]