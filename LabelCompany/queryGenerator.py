from os import listdir
import re
from nltk import word_tokenize
from nltk.corpus import stopwords
#files = listdir("companyEmbedding") 
file = open("companyEmbedding/china_auto_logistics_inc", 'r', encoding='utf8')

queryStr = file.read().replace("\n"," ").replace("\t"," ").replace("\r"," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ")
file.close()


re_words = re.compile('\{.*\}' )
dropStrs = re.findall(re_words, queryStr)
if len(dropStrs) != 0:
    for ds in dropStrs:
        queryStr = queryStr.replace(ds,"")

re_words = re.compile('[\d]+')
dropStrs = re.findall(re_words, queryStr)
if len(dropStrs) != 0:
    for ds in dropStrs:
        queryStr = queryStr.replace(ds,"")

i = 0
while i < 10:
    queryStr = queryStr.replace("  "," ")
    i += 1

for word in queryStr.split():
    if b"\xa0" in word.encode() or b'\xee' in word.encode() or "/" in word:
        queryStr = queryStr.replace(word, "")

stops = set(stopwords.words('english'))
queryStr = " ".join([i for i in word_tokenize(queryStr.lower()) if i not in stops])


paramStr =""

paramStr += "<parameters>\n"

paramStr += "<index>index/company</index>\n"

paramStr += "<query>\n"

paramStr += "<number>1</number>\n"
paramStr += "<text>#combine("+queryStr+")</text>\n"
paramStr += "<baseline>method:tfidf</baseline>\n"

paramStr += "</query>\n"
paramStr += "<count>1000</count>\n"

paramStr += "</parameters>"


file = open("Indri/query.txt", 'w', encoding='utf8')
file.write(paramStr)
file.close()

