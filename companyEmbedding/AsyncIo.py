
import aiohttp
import asyncio
import async_timeout
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver

class CompanyCrawler:

    def __init__(self, query):
        self.query = query
        self.companyInfo = ""

    async def fetch_coroutine(self, client, url):
        with async_timeout.timeout(10):
            try: 
                async with client.get(url) as response:
                    assert response.status == 200
                    contentType = str(response.content_type)
                    if 'html' in str(contentType).lower():
                        html = await response.text()
                        soup = BeautifulSoup(html ,'lxml')
                        [x.extract() for x in soup.findAll('script')]
                        [x.extract() for x in soup.findAll('style')]
                        [x.extract() for x in soup.findAll('nav')]
                        [x.extract() for x in soup.findAll('footer')]
                        self.companyInfo += soup.text
                        #print(soup.text)
                    return await response.release()
            except:
                print(url + " Fail!")
 
    async def main(self, loop):

        #driver = webdriver.Chrome()
        driver = webdriver.PhantomJS()
        url = "https://www.bing.com/"
        driver.get(url)
        elem = driver.find_element_by_xpath('//*[@id="sb_form_q"]')
        elem.send_keys(self.query)
        elem = driver.find_element_by_xpath('//*[@id="sb_form_go"]')
        elem.submit()
        html = driver.page_source
        driver.close()

        soup = BeautifulSoup(html, 'lxml')
        Links = soup.find_all('a')

        Goodlinks = []
        for link in Links:
            linkstr = str(link)
            if (('http' in linkstr) and ('href' in linkstr) and (not 'href="#"' in linkstr) and (not 'href="http://go.microsoft' in linkstr)and (not 'microsofttranslator' in linkstr)):
                Goodlinks.append(link)

        urls = [link['href'] for link in Goodlinks]
        print(self.query, "Good links have been found!")

        #urls = ['http://python.org',
        #        'http://python.org',
        #        'http://python.org',
        #        'http://python.org',
        #        'http://python.org']


        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
 
        async with aiohttp.ClientSession(loop=loop, headers=headers, conn_timeout=5 ) as client:
            tasks = [self.fetch_coroutine(client, url) for url in urls]
            await asyncio.gather(*tasks)
 
 
    #if __name__ == '__main__':
    #    loop = asyncio.get_event_loop()
    #    loop.run_until_complete(main(loop, query))

    def execute(self):
        loop = asyncio.get_event_loop() 
        loop.run_until_complete(self.main(loop))

