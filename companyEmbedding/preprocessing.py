import re
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
from os import listdir

def preprocessing(companyStr):

    companyStr = companyStr.replace("\n"," ").replace("\t"," ").replace("\r"," ")

    i = 0
    while i < 30 :
        companyStr = companyStr.replace("  "," ")
        i+=1

    #re_words = re.compile(u"[\u4e00-\u9fa5]+")  ##drop chinese 
    re_words = re.compile(u"[\u3400-\u9FFF]+") ##drop chinese korean japanese
    dropStrs = re.findall(re_words, companyStr)
    if len(dropStrs) != 0:
        for ds in dropStrs:
            companyStr = companyStr.replace(ds,"")

    re_words = re.compile('\{.*\}' )
    dropStrs = re.findall(re_words, companyStr)
    if len(dropStrs) != 0:
        for ds in dropStrs:
            companyStr = companyStr.replace(ds,"")

    re_words = re.compile('[\d]+')
    dropStrs = re.findall(re_words, companyStr)
    if len(dropStrs) != 0:
        for ds in dropStrs:
            companyStr = companyStr.replace(ds,"")

    for pun in string.punctuation+"©":
        companyStr = companyStr.replace(pun, "")

    stops = set(stopwords.words('english'))
    lemmer = WordNetLemmatizer()


    def isfilter(s):
        return any(not i.encode('utf-8').isalpha() for i in s)

    companyStr = companyStr.lower().strip()
    companyStr.replace('®','')
    wordArr = [lemmer.lemmatize(i) for i in companyStr.split() if ((i not in stops) and (not isfilter(i))) ]
    paramStr = ' '.join(wordArr)

    return companyStr

if __name__ == '__main__': 
    filenames = listdir("companyEmbedding")
    for filename in filenames:
        file = open("companyEmbedding/"+filename, 'r', encoding='utf8')
        fileStr = file.read()
        file.close()
        processedfileStr = preprocessing(fileStr)
        file = open("../LabelCompany/ProcessedCompanyEmbedding/"+filename, 'w', encoding='utf8')
        file.write(processedfileStr)
        file.close()


