from colorama import init
init()
from colorama import Fore, Back, Style
print(chr(27) + "[2J")
print(Fore.YELLOW + 'Loading the scripts ........... ')
print(Style.RESET_ALL)
import re
# identifier = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]{0,30}", re.UNICODE)

from sympy import *
from sympy.solvers import solvers
from sympy import Symbol

# class variable:
# 	version = "1.0"
# 	logs = []
# 	def __init__(self,symbol,name="None",default_value="0",allowed_units=[]):
# 		self.symbol = Symbol(symbol)
# 		self.name = name
# 		self.default_value = default_value
# 		self.allowed_units = allowed_units
# 		self.value = default_value
# 	def showVariableSchema(self):
# 		print("Variable (Name/Symbol -> Unit Allowed/ Default Value) : ",self.name,"/",self.symbol,"/",self.allowed_units,"/",self.default_value)
# 	def showLogs(self):
# 		print(logs)
# 	def setVariables(self,value):
# 		self.value = value



		
class formula:
	version = "1.0"
	logs = []
	def __init__(self,formula_string,domain):
		import re
		self.formula_string = formula_string #Raw formula string
		self.domain = domain #Domain Set

		self.lhs, self.rhs = formula_string.split("=")
		self.lhs = '('+self.lhs+')'.strip()
		self.rhs = '('+self.rhs+')'.strip()
		self.standard_formula = self.lhs+'-'+self.rhs

		self.identifier = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]{0,30}", re.UNICODE)
		self.all_variables = re.findall(self.identifier, self.formula_string) #All variables in a list
		
		#Main Variables
		self.variables = {} #All variables in 'Symbol' formatted 
		
		for identifier in self.all_variables:
			self.variables[identifier] = Symbol(identifier)

		#Main Formula

		for 

	def showFormulaSchema(self):
		print("Standard Formula : ",self.standard_formula)
		print("Participating Variables : ",self.all_variables)

	def calculateRelevanceScore(self,ask_variables):
		a = set(ask_variables)
		b = set(self.all_variables)
		similarity_score = len([i for i, j in zip(a, b) if i == j])
		return similarity_score

class domain:
	version = "1.0"
	logs = []
	def __init__(self,domain_name):
		self.domain_name = domain_name
		self.formula = {}
		self.counter = 1
	def addFormula(self,formula_string):
		self.formula[self.counter] = formula(formula_string,self.domain_name)
		self.counter = self.counter + 1
	def showInformation(self):
		print(self.domain_name)


simple_interest = domain('simple_interest')
simple_interest.showInformation()
simple_interest.addFormula("SI = P*R*T/100")
simple_interest.addFormula("A = P + SI")

for index in simple_interest.formula:
	formula = simple_interest.formula[index]
	print(formula.showFormulaSchema())





