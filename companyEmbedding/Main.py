from BingCrawler import companyEmbedding
import pandas as pd
import string
import os

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
    companyInfo = companyEmbedding(company+" product")
    exclude = set(string.punctuation)
    companyName = ''.join(p for p in company if p not in exclude)
    companyName = companyName.replace(" ", "_").lower()
    file = open("companyEmbedding/"+companyName, 'w', encoding='utf8')
    file.write(companyInfo)
    file.close()

