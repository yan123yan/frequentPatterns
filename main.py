#! encoding utf-8
'''
'''

import LSH
import readNewsFiles

import Apriori

if __name__ == '__main__':
    data_ls = readNewsFiles.get_news_data()

    array = LSH.Shingling(data_ls)
    signature_ls, rowNums = LSH.minHash(array)
    LSH.computeJaccardSimilarityAfterMinhash(signature_ls)

    s = 0.60  # similarity threshold
    r = 20  # rows per band
    bandNum = int(rowNums / r)
    print(bandNum)


    #buckets = LSH.MyLSHashing(signature_ls,bandNum,s,r)
    # buckets = LSH.MylocalitySensitiveHashing(signature_ls,bandNum,s,r)

    buckets = LSH.localitySensitiveHashing(signature_ls,bandNum,s,r)
    I_set_list = LSH.buckets_sort(buckets)

    for ii in I_set_list:
        print(ii)

    buckets_dict = LSH.hash_buckets(I_set_list)

    for i in buckets_dict:
        print(i,buckets_dict[i])

    #Apriori Method
    dataset = Apriori.loadDataSet(buckets_dict)
    C1 = Apriori.createC1(dataset)
    print("C1:")
    print(C1)
    D = list(map(set,dataset))
    print("D:")
    print(D)
    #L1, supportData0 = Apriori.scanD(D,C1, minSupport = 0.5)
    L, supportData = Apriori.apriori(dataset,minSupport=0.5)
    rules = Apriori.generateRules(L, supportData)
    print("*"*100)
    print(L)
    print("*"*100)
    print(supportData)
    print("*" * 100)
    print(rules)


    # transactionDatabase = FPP.toTransactionDatabase(I_set_list)
    # print("-"*100)
    # for j in transactionDatabase:
    #     print(j)