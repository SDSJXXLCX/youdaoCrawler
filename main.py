from urllib import request
from lxml import etree
from urllib.parse import quote
import time
import json
from tqdm import tqdm
import logging

import logging
logger = logging.getLogger("simple_example")
logger.setLevel(logging.DEBUG)
# 建立一个filehandler来把日志记录在文件里，级别为debug以上
fh = logging.FileHandler("words_logging.log")
fh.setLevel(logging.DEBUG)
# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
#将相应的handler添加在logger对象中
logger.addHandler(fh)




def youdao_getHTML(word):
    # 主要时间用于访问网页 页内查找时间占比很小
    # 时间比约为 93-69：2

    url = r"https://dict.youdao.com/result?word={}&lang=en".format(quote(word))
    # print("查找: ", url)
    logger.info("search: {} utl: {}".format(word,url))
    rsp = request.urlopen(url)
    html = rsp.read()
    html = etree.HTML(html)
    return word, html


def youdao_gettr(word, html):
    # print(word)
    tr_list = html.xpath('//*[@id="catalogue_author"]/div[2]/div/div[1]/ul/li')
    num = len(tr_list)
    trans_list = []
    for i in range(num):
        tr = html.xpath('//*[@id="catalogue_author"]/div[2]/div/div[1]/ul/li[{}]/span/text()'.format(i + 1))
        # Xpath中列表以 1 开始
        if len(tr) > 1:
            trans = str(tr[0]) + str(tr[1])
        else:
            trans = str(tr)
        trans_list.append(trans)
    return {
        word: {'num': len(trans_list),
               'trans': trans_list}
    }


def youdao(word):
    word, html = youdao_getHTML(word)
    return youdao_gettr(word, html)


def timeTest(fun, args):
    st = time.time()
    fun(args)
    et = time.time()
    print(et - st)


#
# word = 'Long'
# timeTest(youdao,word)

def saveJsopn(dict,path):
    with open(path,'w',encoding='utf-8') as f:
        # json.dump(dict,f)
        str_ = json.dumps(dict, ensure_ascii=False)  # TODO：dumps 使用单引号''的dict ——> 单引号''变双引号"" + dict变str
        # print(type(str_), str_)
        f.write(str_)
        logger.info("save json. in {}".format(path))

def main():
    dict = {}
    with open('./coca_refined.txt', 'r') as file:
        words = file.readlines()

        for i in tqdm(range(len(words))):
            # print(word.strip())
            word = words[i].strip()
            dict.update(youdao(word))
            if (i+1)%50 == 0:
                path = "./trans/{}_{}.json".format(i-49,i+1)
                saveJsopn(dict,path)
                dict = {}
        path = "./trans/{}_{}.json".format(i - 49, i + 1)
        saveJsopn(dict, path)
        dict = {}

    # print(dict)


def load():
    with open('test.json', 'r', encoding='utf-8') as f:
        data = f.readline().strip()
        print(type(data), data)
        dict = json.loads(data)
        print(type(dict), dict)

if __name__ == "__main__":
    main()
