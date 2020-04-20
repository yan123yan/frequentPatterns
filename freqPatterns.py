import glob
import Apriori
import FPGrowth

path = r'Y:\课程\数据挖掘课件\project1\bbc_news_fulltext\bbc\business'
stop_words_path = r'Y:\课程\数据挖掘课件\project1\stopwords.txt'
# 计算文件夹下的个数
count = len(glob.glob(path + '\*.txt'))
filesList = glob.glob(path + '\*.txt')

def readFile(k=2):
    # 循环获取每个txt内的文章内容并分词
    result_list = []

    stop_words = []
    with open(stop_words_path,'r',encoding='unicode_escape') as ff:
        lines = ff.readlines()
        for line in lines:
            stop_words.append(line.lower().split()[0])

    for each_file in filesList:

        with open(each_file, "r", encoding='unicode_escape') as f:
            data = f.read().replace('\n','').replace(',','').replace('\'','').replace('\"','').replace('.','').replace('?','').replace('!','').replace(')','').replace('(','').lower().split()
            print(data)
            print("len of origin data: ",len(data))
            delete_num = 0
            # 去停用词
            pop_list = []
            for h in range(len(data)):
                for p in stop_words:
                    if data[h] == p:
                        pop_list.append(data[h])
                        #print(p)
                        delete_num = delete_num + 1
            #删除停用词
            for u in pop_list:
                data.remove(u)
                print("delete word:" + u)

            print(data)
            print("delete number is: ",delete_num)
            print("len of new data: ",len(data))

            if k == 1:
                data_list = data
            else:

                final_list = []

                for i in range(len(data)-k+1):
                    str = ""
                    for n in range(0,k):
                        str = str + data[i+n]
                        if n != k-1:
                            str = str + " "
                    final_list.append(str)
                data_list = final_list

        result_list.append(data_list)
    return result_list

result = readFile(k=4)

# Apriori Method
# L, supportData = Apriori.apriori(result, minSupport=0.05)
# rules = Apriori.generateRules(L, supportData)
# print(L)
# print(supportData)
# print(rules)
# print("count Apriori: " + str(len(rules)))

# FPGrowth

initSet = FPGrowth.createInitSet(result)
myFPtree, myHeaderTab = FPGrowth.createFPtree(initSet, 8) #用数据集构造FP树，最小支持度10
freqItems = [] # 挖掘FP树
FPGrowth.mineFPtree(myFPtree, myHeaderTab, 8 , set([]), freqItems)
counta = 0
for x in freqItems:
    if len(x) != 1:
        print(x)
        counta = counta + 1
print("count: " + str(counta))