import re
identifier = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]{0,30}", re.UNICODE)
formulas = ['SI=P*R*T/100', 'A=P+SI']
for formula in formulas:
	lhs, rhs = formula.split("=")
	print("For the formula : ",formula)
	print("LHS : ",lhs)
	print("RHS : ",rhs)
	lhs = '('+lhs+')'
	rhs = '('+rhs+')'
	all_variables = re.findall(identifier, formula)
	print(all_variables)
	standard_formula = lhs+'-'+rhs+"=0"
	print("Standard Formula : "+standard_formula)

class variable:
	version = "1.0"
	logs = []
	def __init__(self,symbol,name="None",default_value="0",allowed_units=[]):
		self.symbol = symbol
		self.name = name
		self.default_value = default_value
		self.allowed_units = allowed_units
		self.value = default_value
	def showVariableSchema(self):
		print("Variable (Name/Symbol -> Unit Allowed/ Default Value) : ",self.name,"/",self.symbol,"/",self.allowed_units,"/",self.default_value)
	def showLogs(self):
		print(logs)
	def setVariables(self,value):
		self.value = value



		
class formula:
	version = "1.0"
	logs = []
	def __init__(self,formula_string,domain):
		self.formula_string = formula_string
		self.domain = domain
		self.lhs, self.rhs = formula_string.split("=")
		lhs = '('+lhs+')'
		rhs = '('+rhs+')'
		self.identifier = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]{0,30}", re.UNICODE
		self.all_variables = re.findall(identifier, self.formula_string)
		self.standard_formula = lhs+'-'+rhs+"=0"

	def showFormulaSchema(self):
		print("Standard Formula : ",self.standard_formula)
		print("Participating Variables : ",self.all_variables)

class domain:
	version = "1.0"
	logs = []
	def __init__(self,domain_name):
		self.domain_name = domain_name
		self.formula = {}
		self.counter = 1
	def addFormula(self,forumula_string):
		self.formula[self.counter] = formula_string