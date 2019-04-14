import xlsxwriter

def loadDataSet():
    file = open("T1014D1K.txt")  # 返回一个文件对象
    dataSet = []
    for line in file.readlines():
        curLine = list(map(int,line.strip().split(" ")))  # curLine.type : list
        dataSet.append(curLine)
    print("dataSet:",dataSet)
    file.close()
    return dataSet

def createC1(dataSet):
    C1_dict = {}  # 物品清单
    C1 = []

    for items in dataSet:
        for item in items:
            if item in C1_dict:
                C1_dict[item] += 1.;  #数字当字典的key
            else:
                C1_dict[item] = 1.;

    for key in C1_dict:
        C1.append([key])
    print("C1: ",C1)
    return C1   #list(C1.keys()) 相等于 list(map(frozenset,C1))

# C1 = createC1(dataSet)
# print("C1:",C1)  # C1: [[25], [52], [164], [240], [274]]

def selectLk(dataSet,Ck,minSupport):  #dataSet 原始数据集
    scan = {}   #字典：存候选项集及其支持度
    for tid in dataSet:
        # print("tid:",tid)  # tid: [33, 217, 283, 346, 496, 515, 626]
        for item in Ck:  # item: [29]   [1,2]
            if set(item).issubset(tid):  # 转换list to set 判断是否为原数据集各tid的子集
                item = list(map(str, item))
                item = ','.join(item)
                if item not in scan.keys():
                    scan[item] = 1
                else:
                    scan[item] += 1
    numItems = float(len(dataSet))
    # retList = []  # 频繁项集
    Lk = {}
    supportData = {}  # 候选项集（ssCnt)的支持度的字典
    for key in scan:
        support = scan[key] / numItems
        #supportData[key] = support
        if support >= minSupport:
            Lk[key] = support;
    # return retList,supportData  #retList -> Lk   L1: {'368': 0.08, '120': 0.056}
    return Lk

def createCk(Lk,k):  # Lk:包含k项的频繁项集
    Ck = []
    Lk = list(Lk.keys())
    print("Lk:",Lk)  # Lk: ['368', '120', '283', '766', '529', '217', '177', '354', '684', '829', '460', '438']
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            #前k-2个项相同时，将两个集合合并
            L1 = Lk[i].split(',')  # str to list[str]
            L1 = list(map(int, L1)) #list[str] to list[int]
            L1pre = (L1)[:k-2]
            L1pre.sort();
            L2 = Lk[j].split(',')
            L2 = list(map(int, L2))
            L2pre = (L2)[:k-2]
            L2pre.sort()
            if L1pre == L2pre:
                Ck.append(list(set(L1).union(set(L2))))
    print("Ck: ",Ck)
    return Ck

def apriori(dataSet,minSupport):
    C1 = createC1(dataSet);
    L1 = selectLk(dataSet,C1,minSupport)  #L1 是字典
    L = [L1]
    k = 2
    while(len(L[k-2]) > 0):
        Ck = createCk(L[k-2],k)
        Lk= selectLk(dataSet,Ck,minSupport)
        L.append(Lk)
        k += 1
    return L

from pprint import pprint
dataSet = loadDataSet()   #原始数据集转换为二维list格式
L = apriori(dataSet,0.01)
pprint(L)

# write list[dictionary] to an excel file
workbook = xlsxwriter.Workbook('out.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0
worksheet.write(row, col, "Itemset")
worksheet.write(row, col+1, "Support")
for items in L:
    for key in items.keys():
        row += 1
        worksheet.write(row, col, key)
        worksheet.write(row, col + 1, items[key])

workbook.close()




