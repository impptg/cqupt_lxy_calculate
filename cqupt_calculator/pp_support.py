import re
import pandas as pd

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


# 根据学期 和 班级 返回文件名
def pp_fn(time_str,a,class_str):
    fn = time_str + a + class_str + '.xlsx'
    return fn

# 根据学期 和 班级 合并所有文件
def pp_getAll(time_str,class_list):
    fn1 = pp_fn(time_str,'1', class_list[0])
    fn2 = pp_fn(time_str,'2',class_list[0])
    df1 = pd.read_excel(fn1, sheet_name=0, header=0)
    df2 = pd.read_excel(fn2, sheet_name=0, header=0)
    dff1 = pd.merge(df1,df2,how='outer',left_on='姓名',right_on='姓名')
    for i in range(1, class_list.__len__()):
        fn1 = pp_fn(time_str, '1', class_list[i])
        fn2 = pp_fn(time_str, '2', class_list[i])
        df1 = pd.read_excel(fn1,sheet_name=0,header=0)
        df2 = pd.read_excel(fn2, sheet_name=0, header=0)
        dff2 = pd.merge(df1,df2,how='outer',left_on='姓名',right_on='姓名')
        dff1 = dff1.append(dff2)

    dff1.to_excel(time_str+'all.xlsx')