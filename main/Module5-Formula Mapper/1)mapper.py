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
	def showVariableSchema(self):
		print("Variable (Name/Symbol -> Unit Allowed/ Default Value) : ",self.name,"/",self.symbol,"/",self.allowed_units,"/",self.default_value)
	def showLogs(self):
		print(logs)

x = variable('w','Weight',['kg','g',)
x.showVariableDetails()

		
#class forumula
#
#class domain