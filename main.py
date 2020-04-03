
from concurrent.futures import ThreadPoolExecutor
import shutil
import os
import requests
import xmltodict, json

baseurl='http://cj.wlzy.tv/inc/api_mac_m3u8.php'
u = baseurl+'?ac=videolist&pg='



try:
    shutil.rmtree('./zlog')
    shutil.rmtree('./zdata')
except Exception as e:
    print(e)


try:
    os.mkdir('./zlog')
    os.mkdir('./zdata')
except Exception as e:
    print(e)


def to(n):
    try:
        res = requests.get(u + str(n), timeout=(5, 10))
        a = res.content.decode('utf-8')
        b = json.dumps(xmltodict.parse(a), ensure_ascii=False)
        fh = open('./zdata/' + str(n) + '.json', 'w', encoding='utf-8')
        fh.write(b)
        fh.close()
    except Exception as e:
        print('pg:',n)
        print(e)
        fh = open('./zlog/' + str(n) + '.err', 'a+', encoding='utf-8')
        fh.write(str(e))
        fh.write('\n')
        fh.close()
        print('重发')
        to(n)
 

def getpage():
    try:
        pgn=int(xmltodict.parse( requests.get(u, timeout=(10, 20)).content.decode('utf-8'))['rss']['list']['@pagecount'])+1 
    except Exception as e:
        getpage()
    
    return  pgn


with ThreadPoolExecutor(max_workers=30) as t:  # 创建一个 线程池
    for i in range(1,getpage()):
        t.submit(to, i)



vlist = []
# 总列表
t = {}
# 分类对象
file_names = os.listdir("./zdata/")
#  分页列表

try:
    shutil.rmtree('./class')
except Exception as e:
    print(e)
# 删除  class


def add(i):
    f = open('./zdata/' + i, 'r', encoding='UTF-8')
    a = json.loads(f.read())['rss']['list']['video']
    f.close()
    for c in a:
        vlist.append(c)


# 读入 总列表方法


def sp(movielist, size, path, start):

    start = start + 1
    if (len(movielist) <= 0):
        return
    b = movielist[:size]
    fh = open(path + str(start), 'w', encoding='utf-8')
    fh.write(json.dumps(b, ensure_ascii=False))
    fh.close()

    del movielist[:size]
    sp(movielist, size, path, start)


# 递归 写入 分页后的 数据方法

for i in file_names:
    add(i)
# 初始分页 汇入总列表
print(len(vlist))

# fh = open('./z.json', 'w', encoding='utf-8')
# fh.write(json.dumps(vlist, ensure_ascii=False))
# fh.close()
# # 写出总列表json 到文件 z.json

for i in vlist:
    t[i['type']] = []

for j in vlist:
    t[j['type']].append(j)

# 生成 总分类 数据

fh = open('./t.json', 'w', encoding='utf-8')
fh.write(json.dumps(t, ensure_ascii=False))
fh.close()
# 写出总列表t.json  


for classdirname in t:
    os.makedirs('./class/' + classdirname)
# 创建 分类文件夹
classname = os.listdir('./class/')
fh = open('./class/index.json', 'w', encoding='utf-8')
fh.write(json.dumps(classname, ensure_ascii=False))
fh.close()

for movieclass in t:
    sp(t[movieclass], 36, './class/' + movieclass + '/', 0)
    file_names = os.listdir('./class/' + movieclass + '/')

    for num in range(len(file_names)):
        file_names[num] = int(file_names[num])
    file_names.sort()
    fh = open('./class/' + movieclass + '/index.json', 'w', encoding='utf-8')
    fh.write(json.dumps(file_names, ensure_ascii=False))
    fh.close()

# 创建分类文件夹下的 分页文件
