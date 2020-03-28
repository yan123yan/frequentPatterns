import part1
from datasketch import MinHash, MinHashLSH

def LSH():
    return_result = []
    result = part1.readFile(k=4)
    num_perm = 1024
    '''
    threshold (float)  – Jaccard 距离阈值设定，默认为0.5
    num_perm (int, optional) – 哈希置换函数设定个数，在weighted-MinHash中为样本规模大小。
    params (tuple, optional) – bands 的数量与规模大小。
    '''
    lsh = MinHashLSH(threshold=0.9,num_perm=num_perm) #num_perm=128
    index = 1
    for each in result:
        #每一个each是一个set
        doc = MinHash(num_perm=num_perm)
        for d in each:
            doc.update(d.encode('utf8'))
        lsh.insert(str(index),doc)
        index = index + 1

    for each_doc in result:
        doc_target = MinHash(num_perm=num_perm)
        for e in each_doc:
            doc_target.update(e.encode('utf8'))
        re = lsh.query(doc_target)
        print("Approximate neighbours with Jaccard similarity > 0.35", re)
        return_result.append(re)
    return clean_data(return_result)

def clean_data(ls):
    new_list = []
    for each in ls:
        if len(each) != 1:
            new_list.append(each)
            print("each: ",each)
    return new_list