from BingCrawler import companyEmbedding
import pandas as pd
import string

path = "master.idx"
file = open(path, 'r',encoding='utf8')

companyLi = []
for line in file:
    if "|" in line:
        companyLi.append(line.split("|")[1])
file.close()


count = 0
flag=False
for company in companyLi:
    if count >= 0:
        flag =True
    if count >= 9000:
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

