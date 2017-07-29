from os import listdir

#files = listdir("companyEmbedding") 
file = open("companyEmbedding/china_auto_logistics_inc", 'r', encoding='utf8')

queryStr = file.read().replace("\n"," ").replace("\t"," ").replace("\r"," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ")
file.close()

paramStr =""

paramStr += "<parameters>\n"
paramStr += "<query>#combine("+queryStr+")</query>\n" 
paramStr += "</parameters>"


file = open("Indri/query.txt", 'w', encoding='utf8')
file.write(paramStr)
file.close()
