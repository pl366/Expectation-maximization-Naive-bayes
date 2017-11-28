import random,os,re
from os import walk
from collections import *
def tokenize(text):
    """Break up text into words"""
    return re.findall('[a-z0-9]+',text)

def tokenize_title_body(title,body):
    """Break up text into title and body that do not overlap"""
    return [t for t in tokenize(title)]+[b for b in tokenize(body)]

def read_training_files(filename):
	priors=Counter()
	likelihood=defaultdict(Counter)
	totalFiles=0
	dirpath=os.path.join('classify-text/dataset/')
	for (dira,dirname,filename) in walk(dirpath):
		print(dirname)
		if(len(dirname)!=0):
			for j in dirname:
				print(j)
				print(os.path.join(dirpath,j))
				for(dirpat,dirnam,filenam) in walk(os.path.join(dirpath,j)):
					ranNo=random.randint(80,120)
					print("Fine")
					for k in filenam[:ranNo]:
						print(dirpat)
						#Open each file. Extract Subject and The body
						priors[j.split('.')[-1]] += 1
						print(os.path.join(dirpat,k))
						f=open(os.path.join(dirpat,k),'r')
						text=f.readlines()
						title=""
						body=""
						for i in range(len(text)):
							if text[i].startswith("Subject"):
								title=text[i][10:]
							if text[i].startswith("Lines"):	
								leni=len(text[i])
								for lk in range(0,i):
									leni+=len(text[lk])
								f.seek(leni+1)
								# print("i========",i,"\n\n\n\n\n")
								try:
									body=f.read()
									break
								except:
									body=""
						f.close()
						print("title = ",title,"\nBody= ",body, "\n\n\n\n\n")
						for word in tokenize_title_body(title,body):
							likelihood[j.split('.')[-1]][word]+=1
					print("LIKELIHOODLIKELIHOODLIKELIHOODLIKELIHOODLIKELIHOODLIKELIHOODLIKELIHOODLIKELIHOODLIKELIHOOD for ",j.split('.')[-1]," is " ,likelihood[j.split('.')[-1]],"\n\n")
	print(priors)

read_training_files("asdac")