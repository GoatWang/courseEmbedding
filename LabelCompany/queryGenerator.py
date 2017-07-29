from os import listdir
import re
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

#files = listdir("companyEmbedding") 
file = open("companyEmbedding/china_auto_logistics_inc", 'r', encoding='utf8')

queryStr = file.read().replace("\n"," ").replace("\t"," ").replace("\r"," ")
file.close()

i = 0
while i < 30 :
    queryStr = queryStr.replace("  "," ")
    i+=1



re_words = re.compile(u"[\u4e00-\u9fa5]+")
dropStrs = re.findall(re_words, queryStr)
if len(dropStrs) != 0:
    for ds in dropStrs:
        queryStr = queryStr.replace(ds,"")

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

for pun in string.punctuation+"©":
    queryStr = queryStr.replace(pun, "")

stops = set(stopwords.words('english'))
lemmer = WordNetLemmatizer()


def isfilter(s):
    return any(not i.encode('utf-8').isalpha() for i in s)

queryStr = queryStr.lower().strip()
queryStr.replace('®','')
wordArr = [lemmer.lemmatize(i) for i in queryStr.split() if ((i not in stops) and (not isfilter(i))) ]
paramStr = ' '.join(wordArr)


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

