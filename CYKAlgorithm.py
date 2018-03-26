import sys
import numpy as np

CHOICE = 0

#Some grammars, and two test examples for each
GRAMMARS = ['Grammar1.txt', 'Grammar2.txt', 'Grammar3.txt']
TESTSTRINGS = [('baaba','babba'),('aaabbb','aaabb'),('she eats a fish with a fork','she eats with a fork a fish')]

GRAMMARPATH = GRAMMARS[CHOICE]
CORRECTTESTSTRING = TESTSTRINGS[CHOICE][0]
INCORRECTTESTSTRING = TESTSTRINGS[CHOICE][1]

def getProduction(grammarPath):
	productions = []
	grammar = open(grammarPath).read()
	p = (grammar.split("PRODUCTIONS:\n")[1].replace("\n", ",").split(','))

	for rule in p:
		left = rule.split(' -> ')[0]
		right = rule.split(' -> ')[1].split(' | ')
		for element in right:
			productions.append((left, element))

	return productions

def getVariables(grammarPath):
	grammar = open(grammarPath).read()
	variables = (grammar.split("VARIABLES:\n")[1].split("PRODUCTIONS:\n")[0].replace("VARIABLES\n","").replace("\n", "").split(' '))

	return variables

def getTerminals(grammarPath):
	grammar = open(grammarPath).read()
	terminals = (grammar.split("VARIABLES:\n")[0].replace("TERMINALS:\n","").replace("\n","").split(' '))
	
	return terminals

def wordsIn(s, terms):
	if ' ' in s:
		splits = s.split(' ')
		return len(splits)
	else:
		return len(s)

def unitProductionUpdate(symbol, symbolPos, rules, variables, table):
	for rule in rules:
		if symbol == rule[1]: #si potrebbe anche usare ==, ma ci sono casi in cui la stessa lettera presente uno spazio (che viene salvato all'inizio) e quindi non sono uguali, anche se idealmente lo sono
			#print(symbol)
			varPos = variables.index(rule[0])
			table[0,symbolPos,varPos] = 1

def productionUpdate(rules, variables, terminals, table, l, s, p):
	for rule in rules:

		left = rule[0] #it should works, assuming CNF grammars.
		leftPos = variables.index(left)

		right = rule[1]

		if right not in terminals:
			right1 = right.split(' ')[0]
			right2 = right.split(' ')[1]
			right1Pos = variables.index(right1)
			right2Pos = variables.index(right2)

			if table[p, s, right1Pos] == 1 and table[l-p-1, s+p+1, right2Pos] == 1:
				table[l,s,leftPos] = 1

		"""if len(right) == 2:

			right1Pos = variables.index(right[0])
			right2Pos = variables.index(right[1])

			if table[p, s, right1Pos] == 1 and table[l-p-1, s+p+1, right2Pos] == 1:
				table[l,s,leftPos] = 1
"""	
		
def YCKAlgorithm(string, pRules, var, terms):
	N = wordsIn(string, terms)

	P = len(var)
	result = False

	#Table initialization
	table = np.zeros((N,N,P)) # zeros corresponds to False

	#Analyzing substrings with length 1
	if ' ' in string:
		splits = string.split(' ')
		for s in range(1, N+1):
			unitProductionUpdate(splits[s-1], s-1, pRules, var, table)
	else:
		for s in range(1, N+1):
			unitProductionUpdate(string[s-1], s-1, pRules, var, table)

	#Analyzing substrings with length greater than 1, until N
	for l in range(2,N+1): 
		for s in range(1,N-l+2): #mi dice quante sottostringhe di lunghezza l ci sono (in python l+1, perchè si conta da zero)
			for p in range(1,l): #mi dice quale combinazione dei sottospazi di l sto usando
				productionUpdate(pRules, var, terms, table, l-1, s-1, p-1)

	if table[N-1,0,0] == 1:
		result = True
		print('String \'' + string + '\' belongs to the selected grammar.' )
	else:
		print('String \'' + string + '\' does not belong to the selected grammar.' )

	return result

if __name__ == '__main__':

	terminals = getTerminals(GRAMMARPATH) 
	variables = getVariables(GRAMMARPATH)
	productions = getProduction(GRAMMARPATH)
	
	goodResult = YCKAlgorithm(CORRECTTESTSTRING, productions, variables, terminals)
	badResult = YCKAlgorithm(INCORRECTTESTSTRING, productions, variables, terminals)
