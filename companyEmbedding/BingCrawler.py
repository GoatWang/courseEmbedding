import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def companyEmbedding(Query):


    #url = "https://www.bing.com/search?q=" + Query+"&setlang=en-us"
    #headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    #re = requests.get(url, headers=headers)
    #re.encoding = 'utf8'
    #html = re.text
    
    driver = webdriver.Chrome()
    #driver = webdriver.PhantomJS()
    url = "https://www.bing.com/"
    driver.get(url)
    elem = driver.find_element_by_xpath('//*[@id="sb_form_q"]')
    elem.send_keys(Query)
    elem = driver.find_element_by_xpath('//*[@id="sb_form_go"]')
    elem.submit()
    html = driver.page_source
    #query = driver.current_url.split("?q=")[1].split("&")[0]
    #print(query)
    #url = driver.current_url+"&lf=1&qpvt="+query
    #print(url)
    #driver.get(url)
    #time.sleep(20)
    driver.close()


    soup = BeautifulSoup(html, 'lxml')
    Links = soup.find_all('a')

    Goodlinks = []
    for link in Links:
        linkstr = str(link)
        if (('http' in linkstr) and ('href' in linkstr) and (not 'href="#"' in linkstr) and (not 'href="http://go.microsoft' in linkstr)and (not 'microsofttranslator' in linkstr)):
            Goodlinks.append(link)

    urls = [link['href'] for link in Goodlinks]
    print(Query, "Good links have been found!")

    pagesStr = ""
    for url in urls:
        yahooBid = "tw.bid.yahoo.com" in url and "category" in url
        googleDoc = "docs.google.com" in url
        pdfFile = url.lower().endswith(".pdf")
        docFile = url.lower().endswith(".doc")
        pptFile = url.lower().endswith(".ppt")
        if not pdfFile and not docFile and not pptFile and not googleDoc and not yahooBid:  ##I can't get information from pdf and google doc
            try:
                headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
                #print(url)
                re = requests.get(url, headers=headers, timeout=5)
                if len(re.content) > 600000:
                    continue

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
                soup= BeautifulSoup(re.text,'lxml')

                [x.extract() for x in soup.findAll('script')]
                [x.extract() for x in soup.findAll('style')]
                [x.extract() for x in soup.findAll('nav')]
                [x.extract() for x in soup.findAll('footer')]

                if not soup.text.startswith("%PDF"):
                    pagesStr += soup.text

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
                print(url + " Fail")

    return pagesStr
