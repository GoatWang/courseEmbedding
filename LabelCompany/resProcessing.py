import pandas as pd
import string

file = open("Indri/res.txt", 'r', encoding='utf8')
retrieved = []
for line in file:
    retrieved.append(line.split()[1].replace("companyEmbedding/",""))
file.close()

df = pd.read_csv("labelData/裕日List.csv", index_col=False)
df.columns = ['0','1']
relevant = list(df[df['1']==1]['0'])[:20]

count = 0
for company in relevant:
    exclude = set(string.punctuation)
    companyName = ''.join(p for p in company if p not in exclude)
    companyName = companyName.replace(" ", "_").lower()
    if companyName in retrieved:
        print(companyName)
        count +=1
print(count)