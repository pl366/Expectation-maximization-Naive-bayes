import log
import sys
import re
from collections import Counter,defaultdict
import random

def tokenize(text):
    """Break up text into words"""
    return re.findall('[a-z0-9]+',text)
def tokenize_title_body(text):
    """Break up text into title and body that do not overlap"""
    return ["title:"+t for t in tokenize(title)]+["body:"+b for b in tokenize(body)]




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
						# with open(filename,'r') as f:
    		# 			    for line in f:
    

						for word in tokenize_title_body(parts[2],parts[3]):
							likelihood[parts[1]][word]+=1

    with open(filename) as f:
        for line in f:
            parts=line.split('\t')
            priors[parts[1]]+=1
            for word in tokenize_title_body(parts[2],parts[3]):
                likelihood[parts[1]][word]+=1
    return (priors,likelihood)                      







def get_priors_likelihood_from_file(filename):
	"""Returns the priors and likelihood for the words on the file"""
	priors = Counter()
	likelihood=defaultdict()
	with open(filename) as f:
		for line in f:
			parts=line.split('\t')
			priors[parts[1]] += 1
			# for word in tokenize(parts[2]):
			for word in tokenize_title_body(parts[2], parts[3]):
				likelihood[parts[1]][word] += 1
	return (priors,	likelihood)

def classify_random(line,priors,likelihood):
    """Return a random category"""
    categories=priors.keys()
    return categories[int(random.random()*len(categories))]


def classify_max_prior(line,priors,likelihood):
    """Return the biggest category"""
    return max(priors,key=lambda x:priors[x])


def classify_bayesian(line,priors,likelihood):
	"""Return the class that maximizes the posteriors """
	max_class=(-1E6,'')
	for c in priors.keys():
		p=priors[c]
		# for word in tokenize(line[2]):
		for word in tokenize_title_body(line[2] , line[3]):
			p=p* max(1E-4, likelihood[c][word])

		if p>max_class[0]:
			max_class=(p,c)

	print(max_class)
	return max_class[1]

def get_class_posteriors(line,priors,likelihood):
	"""E-Step: Return the class that maximizes the posteriors """
	max_class = (-1E6,'')
	posteriors=Counter()
	for c in priors.keys():
		p= priors[c]
		# for word in tokenize(line[2]):
		for word in tokenize_title_body(line[2], line[3]):
			p=p*max(1E-4, likelihood[c][word])
		posteriors[c] = p

	total =sum(posteriors.values())
	if(total == 0.0):
		return posteriors
	for i in posteriors.keys():
		posteriors[i] /= total
	return posteriors


def get_lines_from_file(filename):
	return [line.strip().split('\t') for line in open(filename).readlines()]

def relearn_priors_likelihood(plines):
	"""M-Step: Use the E-step's classification to get the priors, likelihood 	"""
	priors=	Counter()
	likelihood = defaultdict(Counter)

	for (posterior,line) in plines:
		for k in posterior.keys():
			priors[k]+=posterior[k]
			# for word in tokenize(line[2]):
			for word in tokenize_title_body(line[2], line[3]):
				likelihood[k][word] += posterior[k]

	return (priors,likelihood)

def get_posterior_from_lines(lines,keys):
	labelled_posteriors = []
	for line in lines:
		posteriors = Counter()
		for k in keys:
			posteriors[k] = 0
		posteriors[line[1]] = 1
		labelled_posteriors.append((posteriors,line))
	return labelled_posteriors


def main():
    training_file=sys.argv[1]
    testing_file=sys.argv[2]
    
    # (priors,likelihood)=read_training_file(training_file)
    (priors,likelihood) = 	get_priors_likelihood_from_file(training_file)

    testing_lines = get_lines_from_file(testing_file)
    training_lines = get_lines_from_file(training_file)
    
    labelled_posteriors = get_posterior_from_lines(training_lines, priors.keys())
    # lines=read_testing_file(testing_file)
    # for line in lines:
    #     if classify(line,priors,likelihood)==line[1]:
    #         num_correct+=1
    # print ("Classified %d correctly out of %d for an accuracy of %f"%(num_correct,len(lines),float(num_correct)/len(lines)))        
    for i in range(10):
    	unlabelled_posteriors = [] #contains posteriors and the line	
    	num_correct = 0

    	#Normalize the likelihood
    	for k in priors.keys():
    		n=float(sum(likelihood[k].values()))
    		for v in likelihood[k].keys():
    			likelihood[k][v] /= n

    	num_lines = len(testing_lines)
    	num_classified = 0
    	for line in testing_lines:
    		classification = classify_bayesian(line,priors,likelihood)
    		num_classified +=1
    		if classification == line[1]:
    			num_correct+=1
			#ESTEP
    		unlabelled_posteriors.append((get_class_posteriors(line,priors,likelihood),line))

    	print ("Classified %d correctly out of %d for an accuracy of %f"%(num_correct,len(testing_lines),float(num_correct)/len(testing_lines)))        
		#M-STEP
    	(priors,likelihood) = relearn_priors_likelihood(labelled_posteriors + unlabelled_posteriors)

