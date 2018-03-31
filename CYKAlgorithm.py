import sys
import numpy as np
from beautifultable import BeautifulTable

CHOICE = 0

#Some grammars, and two test examples for each grammar
GRAMMARS = ['Grammar1.txt', 'Grammar2.txt', 'Grammar3.txt']
TESTSTRINGS = [('baaba','babba'),('aaabbb','aaabb'),('she eats a fish with a fork','she eats with a fork a fish')]

GRAMMARPATH = GRAMMARS[CHOICE]
CORRECTTESTSTRING = TESTSTRINGS[CHOICE][0]
INCORRECTTESTSTRING = TESTSTRINGS[CHOICE][1]

class Node():
	""" Class used to save a Node, with its symbols and its value, so that to represente the parsing trees """
	def __init__(self, symbol, child1 = None, child2 = None, terminal = None):
		""" Method for construction """
		self.symbol = symbol
		self.child1 = child1
		self.child2 = child2
		self.terminal = terminal

	def getSymbol(self):
		""" Method to get the symbol """
		return self.symbol

	def getChild1(self):
		""" Method to get the first Child """
		return self.child1

	def getChild2(self):
		""" Method to get the second  Child """
		return self.child2

	def getTerminal(self):
		""" Method to get the terminal """
		return self.terminal
	def setSymbol(self, symbol):
		""" Method to set the symbol """
		self.symbol = symbol

def getProduction(grammarPath):
	""" Method to save productions in more manageable data """
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
	""" Method to save variables in more manageable data """
	grammar = open(grammarPath).read()
	variables = (grammar.split("VARIABLES:\n")[1].split("PRODUCTIONS:\n")[0].replace("VARIABLES\n","").replace("\n", "").split(' '))

	return variables

def getTerminals(grammarPath):
	""" Method to save variables in more manageable data """
	grammar = open(grammarPath).read()
	terminals = (grammar.split("VARIABLES:\n")[0].replace("TERMINALS:\n","").replace("\n","").split(' '))
	
	return terminals

def wordsIn(s, terms):
	""" Method to count how many terminals are used in the tested string """
	if ' ' in s:
		splits = s.split(' ')
		return len(splits)
	else:
		return len(s)

def unitProductionUpdate(symbol, symbolPos, rules, variables, table):
	""" Method that implements the first pass of the algorithm: this pass wants to resolve productions like Variables -> terminalSymbol """
	for rule in rules:
		if symbol == rule[1]: 
			table[0][symbolPos].append(Node(symbol = rule[0], terminal = rule[1]))


def productionUpdate(rules, variables, terminals, table, l, s, p):
	""" Method that implements the other passes of the algorithm: this passes wants to resolve productions like Variables -> Var1 Var2 """
	for rule in rules:
		left = rule[0] #it should works, assuming CNF grammars.
		leftPos = variables.index(left)

		right = rule[1]

		if right not in terminals:
			child1 = None
			child2 = None
			right1 = right.split(' ')[0]
			right2 = right.split(' ')[1]
			
			parent1Length = len(table[p][s])
			parent1Symbs = []
			for i in range(parent1Length):
				if right1 == table[p][s][i].getSymbol():
					child1 = table[p][s][i]


			parent2Length = len(table[l-p-1][s+p+1])
			parent2Symbs = []
			for i in range(parent2Length):
				if right2 == table[l-p-1][s+p+1][i].getSymbol():
					child2 = table[l-p-1][s+p+1][i]
			if child1 != None and child2 != None:
				table[l][s].append(Node(symbol = left, child1 = child1, child2 = child2))

def printTable(table, string, N):
	t = BeautifulTable()

	firstRow = []
	if ' ' in string:
		splits = string.split(' ')
		for i in range(N):
			firstRow.append(splits[i])
	else:
		for i in range(N):
			firstRow.append(string[i])

	printTable  = [[[] for i in range(N)] for j in range(N)]
	for i in range(N):
		for j in range(N):
			length = len(table[i][j])
			containers = ' '
			for k in range(length):
				if table[i][j][k].getSymbol() not in containers: 
					containers = containers + str(table[i][j][k].getSymbol()) + ' '
			if containers == ' ':
				containers = ' \ '
			printTable[N-i-1][j] = containers

	for i in range(N):
		t.append_row(printTable[i])

	t.append_row(firstRow)

	print(t)

def constructTree(startSymbol, depth = 0):
	tree = ""

	if startSymbol.getChild2() != None:
		tree += constructTree(startSymbol.getChild2(), depth + 1)

	if startSymbol.getTerminal() != None:
		tree += '\n' + "    "*depth + startSymbol.getSymbol() + '->' + startSymbol.getTerminal()
	else:
		tree += "\n" + "    "*depth + startSymbol.getSymbol()


	if startSymbol.getChild1()!= None:
		tree += constructTree(startSymbol.getChild1(), depth + 1)

	return tree

		
def CYKAlgorithm(string, pRules, var, terms):
	""" Method to run the CYK Parsing Algorithm """
	N = wordsIn(string, terms)
	P = len(var)
	result = False

	#Table initialization
	table = [[[] for i in range(N)] for j in range(N)]

	#Analyzing substrings with length 1
	if ' ' in string:
		splits = string.split(' ')
		for s in range(1, N+1):
			unitProductionUpdate(splits[s-1], s-1, pRules, var, table)
	else:
		for s in range(1, N+1):
			unitProductionUpdate(string[s-1], s-1, pRules, var, table)

	#Analyzing substrings with length greater than 1, until N
	for l in range(2,N+1): #l = length of the substring
		for s in range(1,N-l+2): #s = how many substrings of length l are in the tested string. In particular it is used to define the start position of the substrings with length l
			for p in range(1,l): #p let us to consider different combination of sub-spans and it tells us how we split the span generated by l
				productionUpdate(pRules, var, terms, table, l-1, s-1, p-1)

	finalLength = len(table[N-1][0])
	finalVector = []

	a = table[N-1][0]

	for i in range(finalLength):
		finalVector.append(table[N-1][0][i].getSymbol())

	if var[0] in finalVector:
		result = True
		print('String \'' + string + '\' belongs to the selected grammar.' )
		print(' ')
		print('This is the Parsing Table:')
		printTable(table, string, N)
		print(' ')
		print('These are some possible Parsing trees:')
		print('')

		for el in table[N-1][0]: #looking for startSymbol
			if el.getSymbol() == var[0]:
				tree = constructTree(el,0)
				print(tree)
				print('\n\n\n')
	else:
		print('String \'' + string + '\' does not belong to the selected grammar.' )
		print(' ')
		print('This is the Parsing Table:')
		printTable(table, string, N)

	return result

if __name__ == '__main__':

	terminals = getTerminals(GRAMMARPATH) 
	variables = getVariables(GRAMMARPATH)
	productions = getProduction(GRAMMARPATH)
	
	goodResult = CYKAlgorithm(CORRECTTESTSTRING, productions, variables, terminals)
	print('')
	badResult = CYKAlgorithm(INCORRECTTESTSTRING, productions, variables, terminals)
