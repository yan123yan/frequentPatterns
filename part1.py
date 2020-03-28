import glob


path = r'Y:\课程\数据挖掘课件\project2\bbc_news_fulltext\bbc\business'
# 计算文件夹下的个数
count = len(glob.glob(path + '\*.txt'))
filesList = glob.glob(path + '\*.txt')

def get_news_count():
    return count

def readFile(k=1):
    # 循环获取每个txt内的文章内容并分词
    result_list = []
    for each_file in filesList:

        with open(each_file, "r", encoding='unicode_escape') as f:
            data = f.read().replace('\n','').replace(',','').replace('\'','').replace('\"','').replace('.','').replace('?','').replace('!','').replace(')','').replace('(','').lower().split()

            if k == 1:
                data_set = set(data)
            else:

                final_list = []

                for i in range(len(data)-k+1):
                    str = ""
                    for n in range(0,k):
                        str = str + data[i+n]
                        if n != k-1:
                            str = str + " "
                    final_list.append(str)
                    #print(str)
                data_set = set(final_list)

        result_list.append(data_set)
    return result_list


'''
    for each_file in filesList:

        with open(each_file, "r", encoding='unicode_escape') as f:
            data = f.read().replace('\n','').replace(',','').replace('\'','').replace('\"','').replace('.','').replace('?','').replace('!','').replace(')','').replace('(','').lower().split()

            if k == 1:
                data_set = set(data)
            else:
                str = ""
                final_list = []
                time = 0
                for i in range(len(data)):
                    str = str + data[i]
                    if time != k:
                        str = str + " "
                    if time >= k:
                        final_list.append(str)
                        str = ""
                        time = 0
                    time = time + 1
                data_set = set(final_list)
                pass

        result_list.append(data_set)
'''
