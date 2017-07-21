from BingCrawler import companyEmbedding
import pandas as pd
import string

count = 0
flag=False
for company in list(pd.read_json("CompanyList", typ='series', encoding='utf8')):
    if count >= 36000:
        flag = True
    if count >= 45000:
        flag = False
    if flag:
        companyInfo = companyEmbedding(company+" product")
        exclude = set(string.punctuation)
        companyName = ''.join(p for p in company if p not in exclude)
        companyName = companyName.replace(" ", "_").lower()
        file = open("companyEmbedding/"+companyName, 'w', encoding='utf8')
        file.write(companyInfo)
        file.close()
    count+=1

