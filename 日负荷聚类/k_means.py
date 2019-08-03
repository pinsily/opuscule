import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import random

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
	estimator =KMeans(n_clusters=n_cluster)
	data = data.dropna()
	estimator.fit(data)
	return estimator.labels_  # 分类标签 对应天数


def draw_figure(data, n_cluster, label_pred):
	"""画图表

	data: DataFrame 对象，每行表示一天的负荷变化
	n_cluster: 种类数 
	label_pred: 分类标签

	"""
	columns = len(data.columns) # 获取列数，即每天有 columns 个负荷变化

	x = [i for i in range(columns)] # 横坐标

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
	# plt.yticks([y for y in range(0, max_value, int(max_value/10))])

	plt.style.use('ggplot')
	plt.show()


def random_color():
	"""随机生成颜色

	return: 类似 #666666 的颜色字符串
	"""
	color_arr = ['1','2', '3', '4', '5', '6', '7', '8', '9',
		'A', 'B', 'C', 'D', 'E', 'F']
	return '#'+ "".join([random.choice(color_arr) for _ in range(6)])

def main(filename, n_cluster):
	"""main方法封装

	filename: 数据集 每列代表一天的负荷变化
	n_cluster: 种类数

	"""
	data = read_data(filename)
	label_pred = k_means(data, n_cluster)
	draw_figure(data, n_cluster, label_pred)
	#print(data[0][0],data[1][0],data[2][0],data[3][0])
# 传入文件名和分类种数即可
# main("book_1.xlsx", 10)

def chaochao(filename,n_cluster):
	data = read_data(filename)
	data = data.fillna(value='0')
	data_final=[[] for _ in range(364)]						#最终要选择出来每个负荷最大负荷日的负荷曲线
	data_user=[[] for _ in range(364)]						#363个负荷
	data_user_pd=[[] for _ in range(364)]	
	#导引364个负荷最大日负荷-----------------------------------------------------
	for k in range(364):									
		j=0
		for m in range(31):									#导引每个负荷31天的负荷变化
			day=[]											#24小时日负荷曲线
			for n in range(24):								#导引每个负荷每天的负荷变化
				day.append(data[j][k])						
				j+=1
			data_user[k].append(day)						#31天的日负荷曲线集合
		
		# max_val = max([max(day) for day in data_user[k]])
		data_user_pd[k] = pd.DataFrame(data_user[k])			#转换对象
		label_pred = k_means(data_user_pd[k], 2)		#聚类种类【0，1，2，3】
		#挑选最大工作日负荷---------------------------------------------------
		g=0
		for ele in label_pred:
			if ele==0:
				g+=1
		data_user_ww=[[] for _ in range(40)]	
		if g>15:
			for o in range(len(label_pred)):
				if label_pred[o]==0:
					data_user_ww.append(data_user[k][o])
			max_val = max([max(day) for day in data_user_ww if day])
		else:
			for o in range(len(label_pred)):
				if label_pred[o]==1:
					data_user_ww.append(data_user[k][o])
			max_val = max([max(day) for day in data_user_ww if day])
		for p in range(len(label_pred)):
			if max_val==max(data_user[k][p]):
				data_final[k]=data_user[k][p]
		# print(data_final[k])
	#聚类364个负荷曲线---------------------------------------------------
	data_final_pd=pd.DataFrame(data_final)
	label_pred = k_means(data_final_pd, n_cluster)
	#计算种类------------------------------------------------------------
	kind=[[] for _ in range(n_cluster)]
	for q in  range(n_cluster):
		kind[q]=0
	for w in range(len(label_pred)):
		for s in range(n_cluster):
			if label_pred[w]==s:
				kind[s]+=1
	print(kind)
	draw_figure(data_final_pd, n_cluster, label_pred)
	#取出N条代表种类曲线------------------------------------------------
	data_kind=[]				#最终N种负荷曲线
	for y in range(n_cluster):
		data_user_vv=[]
		c=0
		for z in range(len(label_pred)):
			if label_pred[z]==y:
				data_user_vv.append(data_final[z])
				c+=1
		max_vee = max([max(day) for day in data_user_vv if day])
		for a in range(c):
			if max_vee==max(data_user_vv[a]):
				data_kind.append(data_user_vv[a])
	data_kind_pd=pd.DataFrame(data_kind)
	label_pred = k_means(data_kind_pd, n_cluster)
	draw_figure(data_kind_pd, n_cluster, label_pred)

chaochao("book_2.xlsx", 5)


