import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 加载数据（假设文件名为 ecommerce_data.csv）
file_path=r'C:\Users\张宇煊\Downloads\ecommerce_data.csv'
df = pd.read_csv(file_path)
print("数据形状:", df.shape)
print("\n前5行数据:")
print(df.head())
print("\n数据类型:")
print(df.dtypes)
print("\n描述性统计:")
print(df.describe())

# ========== 数据清洗与预处理 ==========

# ========== 数据清洗与预处理 ==========

# 1. 查看缺失值
print("各列缺失值数量:")
print(df.isnull().sum())

# 2. 删除缺失值（缺失比例低于5%时删除行）
if df.isnull().sum().sum() / len(df) < 0.05:
    df = df.dropna()
    print(f"删除缺失值后数据量: {len(df)}")

# 3. 删除重复值
print(f"重复行数量: {df.duplicated().sum()}")
df = df.drop_duplicates()
print(f"去重后数据量: {len(df)}")

# 4. 处理日期格式（注意：Excel可能存储为数字，需特殊处理）
# 如果你的“购买时间”列显示为类似“#####”或数字，用下面方法转换
# 查看前10行，确认格式
print("原始购买时间示例：")
print(df['购买时间'].head(10))

# 尝试自动转换（pandas 2.0+ 已弃用 infer_datetime_format，直接使用）
df['购买时间'] = pd.to_datetime(df['购买时间'], errors='coerce')

# 检查转换失败的记录数
na_count = df['购买时间'].isna().sum()
if na_count > 0:
    print(f"警告：有 {na_count} 条记录的日期转换失败，将被删除")
    df = df.dropna(subset=['购买时间'])

print("转换后日期范围：", df['购买时间'].min(), "至", df['购买时间'].max())

# 如果已经是标准日期字符串，直接用 pd.to_datetime(df['购买时间']) 即可

# 5. 处理消费金额异常值（IQR法）
Q1 = df['消费金额'].quantile(0.25)
Q3 = df['消费金额'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
df = df[(df['消费金额'] >= lower) & (df['消费金额'] <= upper)]
print(f"剔除异常值后数据量: {len(df)}")

# 6. 提取日期特征
df['年份'] = df['购买时间'].dt.year
df['月份'] = df['购买时间'].dt.month
df['日'] = df['购买时间'].dt.day
df['星期'] = df['购买时间'].dt.day_name()

# 商品类别销售总额排行（横向条形图）
category_sales = df.groupby('商品类别')['消费金额'].sum().sort_values()

plt.figure(figsize=(10,6))
bars = plt.barh(category_sales.index, category_sales.values, color='seagreen')
plt.title('各商品类别销售额排行', fontsize=14)
plt.xlabel('销售额（元）')
plt.ylabel('商品类别')
for i, v in enumerate(category_sales.values):
    plt.text(v + 10, i, f'{v:.0f}', va='center')
plt.tight_layout()
plt.show()

# 各城市消费总额前10名
city_sales = df.groupby('用户城市')['消费金额'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))
bars = plt.bar(city_sales.index, city_sales.values, color='steelblue')
plt.title('Top 10 城市销售额对比', fontsize=14)
plt.xlabel('城市')
plt.ylabel('销售额（元）')
plt.xticks(rotation=45)
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
             f'{bar.get_height():.0f}', ha='center', va='bottom')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,5))
plt.hist(df['用户年龄'], bins=20, color='lightcoral', edgecolor='black')
plt.title('用户年龄分布')
plt.xlabel('年龄')
plt.ylabel('人数')
plt.tight_layout()
plt.show()

plt.figure(figsize=(6,6))
sns.boxplot(x='用户性别', y='消费金额', data=df)
plt.title('不同性别消费金额分布')
plt.xlabel('性别')
plt.ylabel('消费金额（元）')
plt.tight_layout()
plt.show()

monthly_sales = df.groupby('月份')['消费金额'].sum()

plt.figure(figsize=(10,5))
plt.plot(monthly_sales.index, monthly_sales.values, marker='o', linewidth=2, color='darkorange')
plt.title('月度销售额趋势')
plt.xlabel('月份')
plt.ylabel('销售额（元）')
plt.xticks(range(1,13))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 清洗数据
df = pd.read_csv(r'C:\Users\张宇煊\Downloads\ecommerce_data.csv')
df['购买时间'] = pd.to_datetime(df['购买时间'])
# 画静态图
plt.bar(df['商品类别'], df['消费金额'])
plt.show()
import streamlit as st
# 清洗数据（逻辑一模一样，只是放在网页里跑）
df = pd.read_csv(r'C:\Users\张宇煊\Downloads\ecommerce_data.csv')
df['购买时间'] = pd.to_datetime(df['购买时间'])

# 在网页上生成一个下拉菜单，让老板自己选想看哪个类别
category = st.selectbox('选择商品类别', df['商品类别'].unique())
# 根据选择动态出图
filtered = df[df['商品类别'] == category]
st.bar_chart(filtered['消费金额'])  # 直接出可悬停的图

df.to_csv('干净电商数据.csv', index=False, encoding='utf-8-sig')