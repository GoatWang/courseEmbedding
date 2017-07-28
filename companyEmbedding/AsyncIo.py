
import aiohttp
import asyncio
import async_timeout
import os
import time
from bs4 import BeautifulSoup
 
 
async def fetch_coroutine(client, url):
    with async_timeout.timeout(10):
        async with client.get(url) as response:
            assert response.status == 200
            html = await response.text()
            soup = BeautifulSoup(html ,'lxml')
            As = soup.find_all('a')
            for a in As:
                try:
                    print(a)
                except:
                    print("----------------------------------Error------------------------------------")
            return await response.release()
 
 
async def main(loop):

    #urls = ['http://www.ntpu.edu.tw/chinese/',
    #        'http://www.ntpu.edu.tw/chinese/',
    #        'http://www.ntpu.edu.tw/chinese/',
    #        'http://www.ntpu.edu.tw/chinese/',
    #        'http://www.ntpu.edu.tw/chinese/']

    urls = ['http://python.org',
            'http://python.org',
            'http://python.org',
            'http://python.org',
            'http://python.org']

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
 
    async with aiohttp.ClientSession(loop=loop, headers=headers, conn_timeout=5 ) as client:
        startTime = time.time()
        tasks = [fetch_coroutine(client, url) for url in urls]
        await asyncio.gather(*tasks)
        finishTime = time.time()
        print(finishTime - startTime)
 
 
if __name__ == '__main__':
    startTime = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    finishTime = time.time()
    print(finishTime - startTime)
