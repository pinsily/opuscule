import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import random


# @Version : 1.0
# @Time    : 2019-03-21 23:30
# @Author  : pinsily
# @File    : load_k_means.py
#
# @Desc	   : 对日负荷数据进行处理并进行k-means聚类，画图显示

def read_data(filename):
    """读取文件并转置

    filename: 数据集 每列代表一天的负荷变化

    return: 转置后的 DataFrame 对象, 每行代表一天的负荷变化
    """
    return pd.read_excel(filename).T


def k_means(data, n_cluster):
    """对数据集进行聚类

    data: DataFrame 对象，每行表示一天的负荷变化
    n_cluster: 种类数

    return: 聚类后的标签
    """
    estimator = KMeans(n_clusters=n_cluster)

    # 2019.04.18 处理归一化后小数情况，填充或者直接删掉
    data = data.fillna(value='0')
    # data = data.dropna()

    estimator.fit(data)
    return estimator.labels_  # 分类标签 对应天数


def draw_figure(data, n_cluster, label_pred):
    """画图表

    data: DataFrame 对象，每行表示一天的负荷变化
    n_cluster: 种类数 
    label_pred: 分类标签

    """
    columns = len(data.columns)  # 获取列数，即每天有 columns 个负荷变化

    x = [i for i in range(columns)]  # 横坐标

    data_list = np.array(data).tolist()

    # 动态随机生成颜色
    color_list = [random_color() for _ in range(n_cluster)]

    dicts = {}
    for j in range(n_cluster):
        dicts[j] = plt.plot

    # 动态生成对应曲线，优化替代下面的 for-if 情况
    for i in range(len(label_pred)):
        dicts[label_pred[i]](x, data_list[i], color_list[label_pred[i]])

    # for i in range(len(label_pred)):
    #     if label_pred[i] == 0:
    #         plt.plot(x, data_list[i], '#e24fff')
    #     if label_pred[i] == 1:
    #         plt.plot(x, data_list[i], 'g')
    #     if label_pred[i] == 2:
    #         plt.plot(x, data_list[i], 'r')
    #     if label_pred[i] == 3:
    #         plt.plot(x, data_list[i], 'k')
    #     if label_pred[i] == 4:
    #         plt.plot(x, data_list[i], 'c')

    # 图形优化
    plt.rcParams['font.sans-serif'] = ['SimHei'] 	# 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False 	    # 用来正常显示负号
    plt.title('负荷日变化聚类图')
    plt.xlabel("负荷值日变化点")
    plt.ylabel("负荷值")
    max_value = int(max(max(row) for row in data_list))

    # 2019.04.18 归一化后不需要
    # plt.yticks([y for y in range(0, max_value, int(max_value / 10))])

    plt.style.use('ggplot')
    plt.show()


def random_color():
    """随机生成颜色

    return: 类似 #666666 的颜色字符串
    """
    color_arr = ['1', '2', '3', '4', '5', '6', '7', '8', '9',
                 'A', 'B', 'C', 'D', 'E', 'F']
    return '#' + "".join([random.choice(color_arr) for _ in range(6)])


def main(filename, n_cluster):
    """main方法封装

    filename: 数据集 每列代表一天的负荷变化
    n_cluster: 种类数

    """
    data = read_data(filename)
    label_pred = k_means(data, n_cluster)
    draw_figure(data, n_cluster, label_pred)


# 传入文件名和分类种数即可
main("book_2.xlsx", 6)
