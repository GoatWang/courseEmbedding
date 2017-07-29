import pandas as pd
from os import listdir
#from os.path import isfile, join

#df = pd.read_csv("LabelData/裕日List.csv", header=None)
#print(df)

files = listdir("companyEmbedding") 
print(len(files))
print(files)

