#! encoding utf-8
'''
reference: https://www.cnblogs.com/maybe2030/p/4953039.html
           https://www.cnblogs.com/yilujuechen/p/4869703.html
           https://blog.csdn.net/liujan511536/article/details/47729721
           https://www.cnblogs.com/fengfenggirl/p/lsh.html

'''
import readNewsFiles
import numpy as np
import csv
import hashlib

def Shingling(ls):

    #创建集合，对所有文章重复项进行去重
    shingles = set()
    for each_dict_1 in ls:
        #print(each_dict['content'])
        news_content = each_dict_1['content']
        for each_content in news_content:
            shingles.add(each_content)
    #print(len(shingles))

    #将去重后的集合转换为list
    shingles_list = list(shingles)
    #将去重后的集合转换为numpy数组，并作为第一行进行叠加
    shingles_array = np.array(shingles_list)

    for each_dict_2 in ls:
        print("正在处理第"+str(each_dict_2['id'])+"文档")
        news_content = each_dict_2['content']
        #创建等同大小的np数组
        doc_result = np.zeros(len(shingles))
        for each_word in news_content:
            #each_word代表每个单词
            index = shingles_list.index(each_word)
            doc_result[index] = 1
        shingles_array = np.vstack((shingles_array,doc_result))

    print(np.shape(shingles_array))
    #np.shape() :(512行, 18787列)
    return shingles_array.T #(512列, 18787行)

def minHash(array):

    #计算原始文档的相似度
    #！未开发
    computeJaccardSimilarity(array[:,1],array[:,2:])

    res = []
    pi = 600
    for i in range(1,pi):
        print("miniHash第" + str(i) + "个document")
        # 对特征矩阵进行随机置换（行置换）
        random_substitution_array = np.random.permutation(array)
        #将随机置换矩阵由浮点型改为整型
        #random_substitution_array = random_substitution_array.astype(int)
        #获得每列的最小哈希
        ls = []
        for column in range(1,random_substitution_array.shape[1]):
            for row in range(0,random_substitution_array.shape[0]):
                #print("结果是："+str(random_substitution_array[row,column]))
                #print(type(random_substitution_array[row,column]))
                if random_substitution_array[row,column] == str(1) or random_substitution_array[row,column] == str(1.0):
                    ls.append(row)
                    #print("进来了，row是："+str(row))
                    break

        print(ls)
        res.append(ls)
    return res, pi

def computeJaccardSimilarity(doc,others):
    #doc指的是需要去对比的那一列
    #others指的是除去需要被对比的其他列
    #此处，该函数用于计算原本高维数据的准确Jaccard相似度
    #用于与最小哈希得到的签名矩阵相似度进行对比
    #以csv的格式打印至本地
    #仅仅计算第一个文档和其他文档相比
    res = []

    for each in others.T:
        if len(each) != len(doc):
            print("doc与others维度不一致")
            print(doc.shape)
            print(each.shape)
            return
        #记录交集数
        intersection = 0
        #记录并集数
        union = 0
        #将doc和others转为list
        #doc = doc.tolist()
        #each = each.tolist() #目的是为了排除字符串的干扰
        #计算交集和并集数量
        for i in range(len(doc)):

            if doc[i] == str(1.0) and each[i] == str(1.0):
                intersection = intersection + 1
                #print("进来了")
                union = union + 1
            elif doc[i] == str(1.0) or each[i] == str(1.0):
                union = union + 1
        if union == 0:
            print("union is zero")
            return
        #计算Jaccard相似度
        sim = intersection / union
        res.append(sim)

    #写入csv记录
    f = open("jaccardSim.csv",'a')
    csv_writer = csv.writer(f)
    csv_writer.writerow(res)
    f.close()
    print("保存相似度的csv成功")

def computeJaccardSimilarityAfterMinhash(signatureList):
    # signatureList指的是计算完成的签名矩阵的二维数组
    # 此处，该函数用于计算最小哈希得到的签名的Jaccard相似度
    # 用于与原数据得到的相似度进行对比
    # 以csv的格式打印至本地
    # 仅仅计算第一个文档和其他文档相比
    res = []

    #将二维数组转为numpy矩阵
    signature_matrix = np.array(signatureList)
    doc1 = signature_matrix[:,0]
    # 总数
    total = doc1.size
    #获取列数并循环
    for i in range(1,np.shape(signature_matrix)[1]):
        compare_doc = signature_matrix[:,i]
        # 记录相同数
        same = 0
        #遍历其中所有元素
        for j in range(total):
            #如果第一个文档的元素和比较文档对应的元素相同，则交集加1
            if doc1[j] == compare_doc[j]:
                same = same + 1
        # 计算Jaccard相似度
        sim = same / total
        res.append(sim)

    # 写入csv记录
    f = open("jaccardSim.csv", 'a+', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(res)
    f.close()
    print("保存相似度的csv成功")

'''
def LSHashing(signatureList,b,r):
    # 将二维数组转为numpy矩阵
    signature_matrix = np.array(signatureList)
    hashBuckets = {}
    # begin and end of band row
    begin, end = 0, r
    # count the number of band level
    count = 0
    while end <= signature_matrix.shape[0]:
        count = count + 1
        #遍历签名矩阵的列
        for colNum in range(signature_matrix.shape[1]):
            #生成hash对象，使用md5
            hashObj = hashlib.md5()
            #计算哈希值
            band = str(signature_matrix[begin: begin + r, colNum]) + str(count)
            hashObj.update(band.encode())
            #使用哈希值作为bucket的标签
            tag = hashObj.hexdigest()
            #更新字典
            if tag not in hashBuckets:
                hashBuckets[tag] = [colNum]
            elif colNum not in hashBuckets[tag]:
                hashBuckets[tag].append(colNum)
        begin = begin + r
        end = end + r
    return hashBuckets

def MyLSHashing(signatureList,bands,s,r):
    # 将二维数组转为numpy矩阵
    signature_matrix = np.array(signatureList)

    #buckets = []
    hashBuckets = {}

    # 循环整个matrix，将其切成bands
    for b in range(bands):
        # 切分矩阵
        matrix = signature_matrix[b * r:(b + 1) * r]
        # 定义一个降维后的数组
        #hashBuckets = {}
        # begin and end of band row
        begin, end = 0, r
        # count the number of band level
        count = 0

        while end <= matrix.shape[0]:
            count = count + 1
            # 遍历签名矩阵的列
            for colNum in range(matrix.shape[1]):
                # 生成hash对象，使用md5
                hashObj = hashlib.md5()
                # 计算哈希值
                band = str(matrix[begin: begin + r, colNum]) + str(count)
                hashObj.update(band.encode())
                # 使用哈希值作为bucket的标签
                tag = hashObj.hexdigest()
                # 更新字典
                if tag not in hashBuckets:
                    hashBuckets[tag] = [colNum]
                elif colNum not in hashBuckets[tag]:
                    hashBuckets[tag].append(colNum)

            begin = begin + r
            end = end + r

        #buckets.append(hashBuckets)

    #return buckets
    return hashBuckets

# # 先获取行数
        # for i in range(np.shape(matrix)[0]):
        #     #获取列数
        #     for j in range(np.shape(matrix)[1]):
        #         target_doc = int(matrix[i][j])
        #         compare_doc_list = matrix[i].tolist()
        #         sameNums = 0
        #         #迭代比较，计算相似度
        #         compare_doc_list[j] = -1
        #         for compare_doc in compare_doc_list:
        #             if target_doc == compare_doc:
        #                 sameNums = sameNums + 1
        #         similarity = sameNums / len(compare_doc_list)
        #         #如果相似度大于阈值，则将它放进同一个桶里
        #         if similarity > s:
def MylocalitySensitiveHashing(signatureList,bands,s,r):
    # 将二维数组转为numpy矩阵
    signature_matrix = np.array(signatureList)

    #定义总的buckets
    buckets = []
    #循环整个matrix，将其切成bands
    for b in range(bands):
        #切分矩阵
        matrix = signature_matrix[b*r:(b+1)*r]
        #定义一个降维后的数组
        hashBuckets = {}
        #先获取列数
        for i in range(np.shape(matrix)[1]):
            #目标列
            target_doc = matrix.T[i].tolist()
            compare_doc_origin_list = matrix.T.tolist()
            compare_doc_origin_list.pop(i)
            compare_doc_list = compare_doc_origin_list
            for j in range(len(compare_doc_list)):
                sameNums = 0
                compare_doc = compare_doc_list[j]
                #compare_doc为其他列
                #target_doc为需要对比的列
                for index in range(len(compare_doc)):
                    if compare_doc[index] == target_doc[index]:
                        sameNums = sameNums + 1
                similarity = sameNums / len(compare_doc)
                # 如果相似度大于阈值，则将它放进同一个桶里
                if similarity > s:
                    # 生成hash对象，使用md5
                    hashObj = hashlib.md5()
                    # 计算哈希值
                    band = str((i,j)) + str((j,i))
                    hashObj.update(band.encode())
                    # 使用哈希值作为bucket的标签
                    tag = hashObj.hexdigest()
                    # 更新字典
                    if tag not in hashBuckets:
                        hashBuckets[tag] = [i]
                    elif i not in hashBuckets[tag]:
                        hashBuckets[tag].append(i)
        buckets.append(hashBuckets)
    return buckets
'''
def localitySensitiveHashing(signatureList,bands,s,r):
    # 将二维数组转为numpy矩阵
    signature_matrix = np.array(signatureList)

    #定义总的buckets
    buckets = []
    #循环整个matrix，将其切成bands
    for b in range(bands):
        #切分矩阵
        matrix = signature_matrix[b*r:(b+1)*r]
        #定义一个降维后的数组
        bucket = []
        #先获取列数
        for i in range(np.shape(matrix)[1]):
            #目标列
            target_doc = matrix.T[i].tolist()
            compare_doc_origin_list = matrix.T.tolist()
            compare_doc_origin_list.pop(i)
            compare_doc_list = compare_doc_origin_list
            for j in range(len(compare_doc_list)):
                sameNums = 0
                compare_doc = compare_doc_list[j]
                #compare_doc为其他列
                #target_doc为需要对比的列
                for index in range(len(compare_doc)):
                    if compare_doc[index] == target_doc[index]:
                        sameNums = sameNums + 1
                similarity = sameNums / len(compare_doc)
                # 如果相似度大于阈值，则将它放进同一个桶里
                if similarity > s:
                    bucket.append((i,j))
        buckets.append(bucket)
    return buckets



def rec(lis):
    result = []
    number_set = set()
    for i, j in lis:
        #print("number_set:  ", number_set)
        # 如果i没有被记录,j也没有被记录
        if i not in number_set and j not in number_set:
            #print("111")
            result.append({i, j})

        # 如果i被记录,j没有被记录
        elif i in number_set and j not in number_set:
            #print("222")
            for m in result:    # m为集合
                if i in m:
                    m.add(j)

        # 如果i没有被记录,j被记录
        elif i not in number_set and j in number_set:
            #print("333")
            for n in result:
                if j in n:
                    n.add(i)

        # 如果i被记录,j也被记录
        else:
            #print("444")
            i_disappear_index = 0
            j_disappear_index = 0
            for k in range(len(result)):
                if i in result[k]:
                    i_disappear_index = k
                if j in result[k]:
                    j_disappear_index = k
            # 判断i,j是否出现在同一集合
            # 如果出现在同一集合,则无需操作
            # 如果出现在不同集合,则把两个集合合并
            # print(i_disappear_index, j_disappear_index)
            if i_disappear_index < j_disappear_index:
                result = result[:i_disappear_index] + [result[i_disappear_index] | result[j_disappear_index]] + \
                         result[i_disappear_index + 1:j_disappear_index] + result[j_disappear_index + 1:]
            elif i_disappear_index > j_disappear_index:
                result = result[:j_disappear_index] + [result[j_disappear_index] | result[i_disappear_index]] + \
                         result[j_disappear_index + 1:i_disappear_index] + result[i_disappear_index + 1:]
        number_set.add(i)
        number_set.add(j)
        #print("result:  ", result)
    return result

def hash_buckets(list):
    hash_bucket_dict = {}
    count = 0
    for each_list in list:
        new_list = []
        for each_set in each_list:
            new_list.append(each_set)

        # 生成hash对象，使用md5
        hashObj = hashlib.md5()
        # 计算哈希值
        band = str(count)
        hashObj.update(band.encode())
        # 使用哈希值作为bucket的标签
        tag = hashObj.hexdigest()

        #写进桶里
        hash_bucket_dict[tag] = new_list

        count = count + 1
    return hash_bucket_dict


def buckets_sort(buckets):
    #将buckets里的元素重新整理排序
    #初始化列表
    buckets_list = []

    for bucket in buckets:
        #获得每一个桶，取出其各个元素
        #创建每一个桶的集合
        buckets_list.append(rec(bucket))

    return buckets_list







