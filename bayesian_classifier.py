#!/usr/bin/env python
# encoding: utf-8

import sys

#ATTRIBUTES
attributes = {'GENDER': 0 , 'MARITAL_STATUS': 1 , 'AGE_BINARY' : 2 , 'EDUCATION': 3 , 'QSR': 4 }

#Load the dataset
def loadDataset(filePath):
	data = []
	f = open(filePath,'r')
	lines = f.readlines()
	for line in lines:
		line = line.strip()
		strings = line.split("\t")
		data.append(strings[1:])
	return data

#Return all possible attribute values of the set
def loadAttributes(dataSet):
	attributes_dict = [ [] for i in range(len(dataSet[0]))]
	for line in dataSet:
		for i in range(len(line)):
			attributes_dict[i].append(line[i])

	attributes_dict = [ list(set(line)) for line in attributes_dict]

	return attributes_dict


#Main Function
def main(args):
	if len(args) < 5:
		print "Insufficient number of parameters: bayesian_classifier.py <datasetPath> <AttributeToPredict> <Pattern> <Show_All_Prob>"
		exit()


	priori = {}

	#attribute to predict
	target_attribute = args[2]

	#Type (0 - Show All Probabilities  1 - Show the predicted class)
	typeOutput = int(args[4])

	#DataSet
	dataSet = loadDataset(args[1])

	#New Pattern
	pattern = args[3]
	pattern = pattern.split(";")
	#Column to predict
	column = attributes[target_attribute]

	#Load the attribute values of the dataSet
	attrSet =loadAttributes(dataSet)

	for i in xrange(len(pattern)):
		if pattern[i] not in attrSet[i]:
			print "Argument invalid: %s " , pattern[i]
			exit()

	#Step 01 Calculation of the priori probability
	priori['Yes']  = 0
	priori['No'] = 0

	total  = len(dataSet)

	for line in dataSet:
		priori[line[column]] +=1


	#Step 02 Calculation of the probability for the training set
	posteriori = {'Yes': {}, 'No': {}}
	for attr in attrSet[:-1]:
		for value in attr:
 			posteriori['Yes'][value] = 0
			posteriori['No'][value] = 0
			for line in dataSet:
				posteriori[line[column]][value] += line.count(value)
			posteriori['Yes'][value] =  posteriori['Yes'][value] / float(priori['Yes'])
			posteriori['No'][value] =  posteriori['No'][value] / float(priori['No'])


	#Step 03 Calculation of the probability for the target pattern
	post = {}

	post['Yes'] = 1.0
	post['No'] = 1.0

	for value in pattern:
		post['Yes'] *= posteriori['Yes'][value]
	 	post['No'] *= posteriori['No'][value]

	post['Yes'] *= (priori['Yes']/ float(total))
	post['No'] *= (priori['No']/ float(total))


	#Prints the output

	if typeOutput:
		#The predicited class
		if post['Yes'] > post['No']:
			print '%s = %s' % (target_attribute,'Yes')
		else:
			print '%s = %s' % (target_attribute,'No')

	else:
		#all probabilities
		for key,value in post.items():
			print 'P(%s=%s) = %f' % (target_attribute,key,value)




if __name__ == '__main__':
	main(sys.argv)

