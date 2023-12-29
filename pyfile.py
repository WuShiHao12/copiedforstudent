import pandas as pd

# 1.设计csv数据
# df = pd.DataFrame({'姓名':['张三','李四','小明','小李'],'英语':[98,62,76,95],'数学':[87,76,98,65],'物理':[92,78,83,72]})
# df.to_csv('score.csv',index=False,encoding='utf-8-sig')

# 2.读取csv数据
df = pd.read_csv('score.csv',index_col=[0],encoding='utf-8-sig')
print(df)

print('\n\n')
# 3.按列统计每门课的最高分和平均分
print('课程最高分:')
print(df.max())
print('\n\n')
print('课程平均分:')
print(df.mean())

# 4.按行统计每个人的数据（最高分和最低分）
print('\n\n')
print('个人的最高分:')
print(df.max(axis=1))
print('\n\n')
print('个人的最低分:')
print(df.min(axis=1))


# 5.提取行索引标签和英语列数据作为柱状图的X轴和Y轴的值,绘制成绩柱状图
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
df.plot(kind='bar',y='英语',rot=0)
plt.show()

