#! encoding utf-8
'''

reference:  https://blog.csdn.net/qq_36523839/article/details/82191677
            https://www.jianshu.com/p/2ee0a247a8cc
            https://blog.csdn.net/u010454729/article/details/49078505
            https://www.cnblogs.com/iupoint/p/11095381.html
            https://www.cnblogs.com/lsqin/p/9342926.html
            https://blog.csdn.net/atmiao/article/details/72903883
'''


#加载并转换数据集
def loadDataSet(buckets_dict):
    new_list = []
    for k in buckets_dict:
        #获取每一行的set
        for each_set in buckets_dict[k]:
            new_list.append(list(each_set))
    print("Transfer to New Result List:")
    print(new_list)
    return new_list

#选取数据集的非重复元素组成候选集的集合C1
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:  # 对数据集中的每条列表
        for item in transaction:  # 对列表中的每个元素
            if [item] not in C1:  # 注意，item外要加上[]，便于与C1中的[item]对比
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))  # 将C1各元素转换为frozenset格式，注意frozenset作用对象为可迭代对象

#由Ck产生Lk：扫描数据集D，计算候选集Ck各元素在D中的支持度，选取支持度大于设定值的元素进入Lk
def scanD(D,Ck,minSupport):
    #print("scanD...")
    ssCnt={}
    for tid in D: #对数据集中的每条购买记录
        for can in Ck: #遍历Ck所有候选集
            if can.issubset(tid): #如果候选集包含在购买记录中，计数+1
                ssCnt[can]=ssCnt.get(can,0)+1
    numItems=float(len(D)) #购买记录数
    retList=[] #用于存放支持度大于设定值的项集
    supportData={} #用于记录各项集对应的支持度
    for key in ssCnt.keys():
        support=ssCnt[key]/numItems
        if support>=minSupport:
            retList.insert(0,key)
        supportData[key]=support
    return retList,supportData

#由Lk产生Ck+1
def aprioriGen(Lk,k): #Lk的k和参数k不是同一个概念，Lk的k比参数k小1
    #print("aprioriGen...")
    retList=[]
    lenLk=len(Lk)
    for i in range(lenLk):
        #print("i:"+str(i))
        for j in range(i+1,lenLk): #比较Lk中的每一个元素与其他元素
            L1=list(Lk[i])[:k-2];L2=list(Lk[j])[:k-2]
            L1.sort();L2.sort()
            if L1==L2: #若前k-2项相同，则合并这两项
                retList.append(Lk[i]|Lk[j])
    return retList

#Apriori算法主函数
def apriori(dataSet,minSupport=0.5):
    C1=createC1(dataSet)
    D=list(map(set,dataSet))
    L1,supportData=scanD(D,C1,minSupport)
    L=[L1]
    k=2
    while len(L[k-2])>0: #当L[k]为空时，停止迭代
        #print("len(L[k-2]):"+str(len(L[k-2])))
        Ck=aprioriGen(L[k-2],k) #L[k-2]对应的值是Lk-1
        Lk,supK=scanD(D,Ck,minSupport)
        supportData.update(supK)
        L.append(Lk)
        k+=1
    return L,supportData

# 主函数，由频繁项集以及对应的支持度，得到各条规则的置信度，选择置信度满足要求的规则为关联规则
# 为了避免将所有数据都对比一遍，采用与上述相同的逻辑减少计算量——一层一层计算筛选
def generateRules(L,supportData,minConf=0.5):
    bigRuleList=[]
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1=[frozenset([item]) for item in freqSet] # H1是频繁项集单元素列表，是关联规则中a->b的b项
            if i>1:
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else:
                calConf(freqSet,H1,supportData,bigRuleList,minConf)
    return bigRuleList

# 置信度计算函数
def calConf(freqSet,H,supportData,brl,minConf=0.5):
    prunedH=[] # 用于存放置信度满足要求的关联规则的b项，即“提纯后的H”
    for conseq in H:
        conf=supportData[freqSet]/supportData[freqSet-conseq]
        if conf>=minConf:
            print (freqSet-conseq,'-->',conseq,'conf:',conf)
            brl.append([freqSet-conseq,conseq,conf])
            prunedH.append(conseq)
    return prunedH

# 关联规则合并函数
def rulesFromConseq(freqSet,H,supportData,brl,minConf=0.5):
    m=len(H[0])
    if len(freqSet)>(m+1): #查看频繁项集freqSet是否大到可以移除大小为m的子集
        Hmp1=aprioriGen(H,m+1) # 从Hm合并Hm+1
        Hmp1=calConf(freqSet,Hmp1,supportData,brl,minConf)
        if len(Hmp1)>1: #若合并后的Hm+1的元素大于1个，则继续合并
            rulesFromConseq(freqSet,Hmp1,supportData,brl,minConf)
