import requests

TargetDirectory = "CourseEmbedding"
#TargetDirectory = input("請輸入目標資料夾: ")
Query = input("請輸入查詢關鍵字: ")

url = "https://www.bing.com/search?q=" + Query + "+簡介"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
re = requests.get(url, headers=headers)
re.encoding = 'utf8'

from bs4 import BeautifulSoup
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
print("Good links have been found!")

#file = open("links", 'w', encoding = 'utf8')
#for url in urls:
#    file.write(url + "\n")
#file.close()


pagesStr = ""
for url in urls:
    print(url.split("/")[2])

    try:
        re = requests.get(url, headers=headers, timeout=5)
        charset = 'utf8'
        #re.encoding = charset

        for line in re.text.split("\n"):
            line = str(line.lower())
            if "charset" in line:
                if 'cp950' in line:
                    charset = 'cp950'
                elif 'big5' in line:
                    charset = 'big5'
                break

        re.encoding = charset
        soup= BeautifulSoup(re.text,'lxml')

        [x.extract() for x in soup.findAll('script')]
        [x.extract() for x in soup.findAll('style')]
        [x.extract() for x in soup.findAll('nav')]
        [x.extract() for x in soup.findAll('footer')]

        if not soup.text.startswith("%PDF") and url.split("/")[2] != "24h.pchome.com.tw":
            pagesStr += soup.text

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

savePath = TargetDirectory + "//" + Query;
file = open(savePath, 'w', encoding='utf8')
file.write(pagesStr)
file.close()