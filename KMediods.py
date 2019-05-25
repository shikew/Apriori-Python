import random
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import pprint

def loadData(fileName):
    file = open(fileName,'r')  # 返回一个文件对象
    items = [];
    for line in file.readlines():
        itemFeatures = []  # 存放每个item的特征值
        line = line.split(' ')
        for j in range(len(line)-1): # 每行最后一个元素为‘\n’，需要去除
            itemFeatures.append(float(line[j])) # str to float
        items.append(itemFeatures)

    random.shuffle(items) #数据随机排序
    file.close()

    return items

def initKMedoids(items,k):
    ItemNum = len(items)
    initIndex = random.sample(range(0,ItemNum),k)  #随机生成不重复的 k 个索引
    print(initIndex)
    medoids = [] #初始化k个中心点
    for i in range(len(initIndex)):
        medoids.append(items[initIndex[i]])
    return medoids

def calDistance(x,y):
    S_dis = 0;
    for i in range(len(x)):
        S_dis += math.pow(x[i]-y[i],2);
    return math.sqrt(S_dis)

def groupItem(medoids,item): #判断当前 item 属于哪个簇
    disList = []
    for i in range(len(medoids)):
        dis = calDistance(medoids[i],item)
        disList.append(dis)
    return disList.index(min(disList)) #返回和自己距离最近的 medoids 的 index

def groupItemDis(medoids,item): #判断当前 item 到最近的簇的距离
    disList = []
    for i in range(len(medoids)):
        dis = calDistance(medoids[i],item)
        disList.append(dis)
    return min(disList) #返回和自己距离最近的 medoids 的 距离

def findKMedoids(k,items,maxIterations = 100000):
    medoids = initKMedoids(items,k)
    # 初始化
    lost = np.ones([len(items), k]) * float('inf') # 损失，每个item 到 各簇的距离
    lost.tolist()
    lostforEach = 0.0
    curLost = 0.0

    #初次划分,所有元素划分到k个簇中
    for j in range(len(items)):
        item = items[j]
        # index = groupItem(medoids,item)
        minDis = groupItemDis(medoids,item)
        curLost += minDis
        # clusterSizes[index] += 1
        # clusterItems[j] = index

    for iter in range(maxIterations): #假设迭代的次数
        for m in range(k): # 遍历 mediods
            orginM = medoids[m] #被替换的中心点
            for i in range(len(items)): # 第1次循环相当于用各item 替换 mediod[0] lost[i,m]
                medoids[m] = items[i]
                for it in range(len(items)):
                    minDis = groupItemDis(medoids,items[it])
                    lost[i,m] += minDis
            medoids[m] = orginM

        minInRow = []
        for i in range(len(lost)):
            minInRow.append(min(lost[i]))
        minLost = min(minInRow)

        if(minLost < curLost):
            curLost = minLost
            #找到最小Lost对应的坐标,并替换
            for i in range(len(lost)):
                for j in range(len(lost[i])):
                    if(lost[i][j] == minLost):
                        medoids[j] = items[i]

        else:
            break

    return medoids

def findClusters(medoids,items):  # 将所有元素依次归类到各簇中
    clusters = [[] for i in range(len(medoids))] #初始化簇

    for item in items:
        index = groupItem(medoids,item);
        clusters[index].append(item)

    return clusters

items = loadData('data.txt')
k = 20
medoids = findKMedoids(k,items)

for i in range(len(medoids)):
    print("medoids",medoids[i])

clusters = findClusters(medoids,items)
# print(k)
# pprint.pprint(medoids)
# print(len(medoids))
for i in range(k):
    print('各cluster中的item个数：',len(clusters[i]))

for i in range(k):
    print('cluster:',clusters[i])

# #降维及可视化
# tsne = TSNE()
# medoids_TSNE = TSNE(learning_rate=100).fit_transform(medoids)
# # items_TSNE = TSNE(learning_rate=100).fit_transform(clusters)
#
# clusters_TSNE = []
# for i in range(k):
#     clusters_TSNE[i] = TSNE(learning_rate=100).fit_transform(clusters[i])
#
# mark = ['or', 'ob', 'og', 'oy','om']
#
# for i in range(k):
#     plt.plot(medoids_TSNE[i][0], medoids_TSNE[i][1], mark[i])
#
# for i in range(len(clusters_TSNE)):
#     for j in range(len(clusters_TSNE[i])):
#         plt.plot(clusters_TSNE[i][j][0], clusters_TSNE[i][j][1], '+c')
#
# plt.show()


