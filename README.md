# cqupt_lxy_calculate
## 再也没有人能算一晚上成绩了
1. 将同一学年所有成绩下载
2. 默认后缀为.xls 手动使用word/wps 改为.xlsx
3. 取消pp_getAll(13行)的注释，运行至该处
4. 打开生成的全部数据的excel 名称为 20xxall.xlsx
5. 在想计算的学科后面添加 _n // _n.m // _.m
6. 例如 A123123数学分析 -> A123123数学分析_5.5
7. 保存，注释pp_getAll(13行)
8. 所得文件 20xxresult.xlsx 即为结果
