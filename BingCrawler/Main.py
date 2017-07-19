import pandas as pd
from BingCrawlerSelenium import courseEmbedding

for course in list(pd.read_json("CourseName", typ='series')):
    TargetDirectory = "CourseEmbedding"
    Query = course
    pagesStr = courseEmbedding(Query, TargetDirectory)

    savePath = TargetDirectory + "//" + Query;
    file = open(savePath, 'w', encoding='utf8')
    file.write(pagesStr)
    file.close()