import pandas as pd
from pymongo import MongoClient
import re
from BingCrawlerSelenium import courseEmbedding

conn = MongoClient('localhost', 27017)
db = conn.SuperUniversityCourses
collection = db['1052ntpu']

#conn = MongoClient("mongodb://jeremy4555:P%40ssw0rd@ds155841.mlab.com:55841/superuniversitycourses")
#db = conn.superuniversitycourses
#collection = db['allcourses']

df = pd.DataFrame([i for i in collection.find()])
courseNameSet = set(df['科目名稱'])

re_words = re.compile(u"[\u4e00-\u9fa5]+")  
chineseNameSet = set(["".join(re.findall(re_words, courseName)) for courseName in courseNameSet])

pd.Series(list(chineseNameSet)).to_json("CourseName", force_ascii=False)

#for course in list(pd.read_json("CourseName", typ='series')):
#    TargetDirectory = "CourseEmbeddingNTPU"
#    Query = course
#    pagesStr = courseEmbedding(Query, TargetDirectory)

#    savePath = TargetDirectory + "//" + Query;
#    file = open(savePath, 'w', encoding='utf8')
#    file.write(pagesStr)
#    file.close()