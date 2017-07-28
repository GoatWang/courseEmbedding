import pandas as pd
import string
import os
from AsyncIo import CompanyCrawler


df = pd.read_csv("crawledCompanyLi")
print("to be crawled:", len(df))

dfSort = df.sort_values(['0'])


beforePart = dfSort[:len(dfSort)//2]
afterPart = dfSort[len(dfSort)//2:]
print("beforePart Length", len(beforePart))
print("afterPart Length", len(afterPart))
print(len(beforePart) + len(afterPart))

print("First Start Data")
print(dfSort.xs(0))
print("Second Start Data")
print(dfSort.xs(len(dfSort)//2))


for company in beforePart['0']:
    crawler = CompanyCrawler(company+" product")
    crawler.execute()
    
    exclude = set(string.punctuation)
    companyName = ''.join(p for p in company if p not in exclude)
    companyName = companyName.replace(" ", "_").lower()

    #file = open("Test/" + companyName, 'w', encoding='utf8')
    file = open("companyEmbedding/" + companyName, 'w', encoding='utf8')
    file.write(crawler.companyInfo)
    file.close()

