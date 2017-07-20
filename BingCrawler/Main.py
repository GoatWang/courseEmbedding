import pandas as pd
from BingCrawlerSelenium import courseEmbeddingSelenium
from BingCrawlerRequests import courseEmbeddingRequests
from BingCrawler import courseEmbedding 

flag = True
for course in list(pd.read_json("CourseName", typ='series', encoding='utf8')):
    if course == "邏輯思考概論":
        flag = True
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
