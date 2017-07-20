import requests
from langconv import *
from bs4 import BeautifulSoup


def courseEmbeddingRequests(Query, TargetDirectory = "CourseEmbedding"):

    #TargetDirectory = "CourseEmbedding"
    #TargetDirectory = input("請輸入目標資料夾: ")
    #Query = input("請輸入查詢關鍵字: ")

    url = "https://www.bing.com/search?q=" + Query + "+簡介"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    re = requests.get(url, headers=headers)
    re.encoding = 'utf8'

    html = re.text
    soup = BeautifulSoup(html, 'lxml')
    Links = soup.find_all('a')

    Goodlinks = []
    for link in Links:
        if (
    not 'search' in str(link) and not 'Bing' in str(link) and not 'images' in str(link) and not 'maps' in str(link) 
    and not '喜好設定' in str(link) and not '地區' in str(link) and not '語言' in str(link) and not '日期' in str(link)
    and not '設定檔圖片' in str(link) and not '登入' in str(link) and not '網路' in str(link) and not '我儲存的項目' in str(link)
    and not '隱私權和' in str(link) and not '法律聲明' in str(link) and not '關於我們的廣告' in str(link) 
    and not '意見反應' in str(link) and not '廣告' in str(link) and not '說明' in str(link) and not 'sb_pagS' in str(link) 
           ):
            Goodlinks.append(link)

    urls = [link['href'] for link in Goodlinks]
    print(Query, "Good links have been found!")

    pagesStr = ""
    for url in urls:
        yahooBid = "tw.bid.yahoo.com" in url and "category" in url
        googleDoc = "docs.google.com" in url
        pdfFile = url.endswith(".pdf")
        docFile = url.endswith(".doc")
        pptFile = url.endswith(".ppt")
        if not pdfFile and not docFile and not pptFile and not googleDoc and not yahooBid:  ##I can't get information from pdf and google doc
            try:
                re = requests.get(url, headers=headers, timeout=5)
                charset = 'utf8'
                re.encoding = charset

                for line in re.text.split("\n"):
                    line = str(line.lower())
                    if "charset" in line:
                        if 'cp950' in line:
                            charset = 'cp950'
                        elif 'big5' in line:
                            charset = 'big5'
                        break

                re.encoding = charset
                soup= BeautifulSoup(re.text,'lxml', from_encoding=charset)

                [x.extract() for x in soup.findAll('script')]
                [x.extract() for x in soup.findAll('style')]
                [x.extract() for x in soup.findAll('nav')]
                [x.extract() for x in soup.findAll('footer')]

                def Simplified2Traditional(sentence):
                    '''
                    将sentence中的简体字转为繁体字
                    :param sentence: 待转换的句子
                    :return: 将句子中简体字转换为繁体字之后的句子
                    '''
                    sentence = Converter('zh-hant').convert(sentence)
                    return sentence
            
                if not soup.text.startswith("%PDF") and url.split("/")[2] != "24h.pchome.com.tw":
                    pagesStr += Simplified2Traditional(soup.text)

                #pagesStr += "\n ------------------------------------- \n"
                #pagesStr += "\n ------------------------------------- \n"
                #pagesStr += "\n ------------------------------------- \n"
                #pagesStr += "\n" + charset +"\n"
                #pagesStr += "\n" + url +"\n"
                #pagesStr += "\n ------------------------------------- \n"
                #pagesStr += "\n ------------------------------------- \n"
                #pagesStr += "\n ------------------------------------- \n"
                #print(url.split("/")[2] + "success")
            except:
                print(url.split("/")[2] + "Fail")

    return pagesStr
