#! encoding utf-8
import part2
import Apriori
import FPGrowth

if __name__ == '__main__':
    #get buckets
    dataset = part2.LSH()

    # Apriori Method

    L, supportData = Apriori.apriori(dataset, minSupport=0.05)
    rules = Apriori.generateRules(L, supportData)
    print(L)
    print(supportData)
    print(rules)
    print("count Apriori: " + str(len(rules)))

    # FPGrowth

    initSet = FPGrowth.createInitSet(dataset)
    myFPtree, myHeaderTab = FPGrowth.createFPtree(initSet, 2) #用数据集构造FP树，最小支持度10
    freqItems = [] # 挖掘FP树
    FPGrowth.mineFPtree(myFPtree, myHeaderTab, 2, set([]), freqItems)
    count = 0
    for x in freqItems:
        if len(x) != 1:
            print(x)
            count = count + 1
    print("count: " + str(count))