import pandas as pd
import string
import os

path = "master.idx"
file = open(path, 'r',encoding='utf8')

companyLi = []
for line in file:
    if "|" in line:
        companyLi.append(line.split("|")[1])
file.close()
companyLi = list(set(companyLi))


#with open('companyList', 'w', encoding='utf-8') as file:
#    pd.Series(companyLi).to_json(file, force_ascii=False)

df = pd.DataFrame(companyLi)
df.columns = [['name']]

crawledCompanies = os.listdir("companyEmbedding")
#print(len(crawledCompanies))

def filenameGenerate(row):
    exclude = set(string.punctuation)
    companyName = ''.join(p for p in row['name'] if p not in exclude)
    companyName = companyName.replace(" ", "_").lower()
    if not companyName in crawledCompanies:
        return str(row['name'])
df = df.apply(filenameGenerate,axis=1)
df = df[pd.notnull(df)]
df = pd.DataFrame(df)
#print(df)
df.to_csv("crawledCompanyLi", index=False)


