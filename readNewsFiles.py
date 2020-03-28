
import glob

path = r'Y:\课程\数据挖掘课件\project2\bbc_news_fulltext\bbc\sport'
#计算文件夹下的个数
count = len(glob.glob(path+ '\*.txt'))
filesList = glob.glob(path+ '\*.txt')

#循环获取每个txt内的文章内容并分词
def get_news_data():
    ls = []
    times = 1
    for each_file in filesList:
        dict = {}
        dict['id'] = times
        with open(each_file,"r",encoding='unicode_escape') as f:
                data = f.read()
                dict['content'] = data.replace('\n',' ').split()
        times = times + 1
        ls.append(dict)
    return ls

def get_news_count():
    return count

#打印获得的数据列表
def print_ls():
    ls = get_news_data()
    for a in ls:
        print(a)


