from selenium import webdriver
import time
from bs4 import BeautifulSoup
from langconv import *

def courseEmbeddingSelenium(Query, TargetDirectory = "CourseEmbedding"):

    driver = webdriver.Chrome()
    #driver = webdriver.PhantomJS()
    url = "https://www.bing.com/"
    driver.get(url)
    elem = driver.find_element_by_xpath('//*[@id="sb_form_q"]')
    elem.send_keys(Query)
    elem = driver.find_element_by_xpath('//*[@id="sb_form_go"]')
    elem.submit()
    html = driver.page_source


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


    ## 簡轉繁
    def Simplified2Traditional(sentence):
        '''
        将sentence中的简体字转为繁体字
        :param sentence: 待转换的句子
        :return: 将句子中简体字转换为繁体字之后的句子
        '''
        sentence = Converter('zh-hant').convert(sentence)
        return sentence


    pagesStr = ""
    for url in urls:
        yahooBid = "tw.bid.yahoo.com" in url and "category" in url
        googleDoc = "docs.google.com" in url
        pdfFile = url.endswith(".pdf")
        docFile = url.endswith(".doc")
        pptFile = url.endswith(".ppt")
        if not pdfFile and not docFile and not pptFile and not googleDoc and not yahooBid:  ##I can't get information from pdf and google doc
            try:
                driver.get(url)
                driver.implicitly_wait(2)
                html = driver.page_source

                charset = 'utf8'
                for line in html.split("\n"):
                    line = str(line.lower())
                    if "charset" in line:
                        if 'cp950' in line:
                            charset = 'cp950'
                        elif 'big5' in line:
                            charset = 'big5'
                        break

                soup= BeautifulSoup(html,'lxml')
                if soup.find("embed") == None or not ".pdf" in soup.find("embed")['src']:  ##Some server will directly return pdf file, which I can't get information from.
                    soup.encode = charset

                    [x.extract() for x in soup.findAll('script')]  ##take off script part
                    [x.extract() for x in soup.findAll('style')]  ##take off script style
                    [x.extract() for x in soup.findAll('nav')]  ##take off script nav
                    [x.extract() for x in soup.findAll('footer')]  ##take off script footer

                    pagesStr += Simplified2Traditional(soup.text)
                    #pagesStr += "\n ------------------------------------- \n"
                    #pagesStr += "\n ------------------------------------- \n"
                    #pagesStr += "\n ------------------------------------- \n"
                    #pagesStr += "\n" + charset +"\n"
                    #pagesStr += "\n" + url +"\n"
                    #pagesStr += "\n ------------------------------------- \n"
                    #pagesStr += "\n ------------------------------------- \n"
                    #pagesStr += "\n ------------------------------------- \n"
                    print("success")
            except:
                print("Fail")


    driver.close()

    return pagesStr
    #savePath = TargetDirectory + "//" + Query;
    #file = open(savePath, 'w', encoding='utf8')
    #file.write(pagesStr)
    #file.close()