import pandas as pd
from BingCrawlerSelenium import courseEmbeddingSelenium
from BingCrawlerRequests import courseEmbeddingRequests
from BingCrawler import courseEmbedding 

flag = False
count = 0
for course in list(pd.read_json("CourseName", typ='series', encoding='utf8')):
    if course == "歐洲文學概論":
        flag = True
    if count >6500:
        flag = False
    if flag:
        TargetDirectory = "CourseEmbedding"
        Query = course
        try:
            #pagesStr = courseEmbeddingRequests(Query, TargetDirectory)
            #pagesStr = courseEmbeddingSelenium(Query, TargetDirectory)
            pagesStr = courseEmbedding(Query, TargetDirectory)
        except:
            print(course, "Fail")
            continue

        savePath = TargetDirectory + "//" + Query;
        file = open(savePath, 'w', encoding='utf8')
        file.write(pagesStr)
        file.close()
    count +=1
