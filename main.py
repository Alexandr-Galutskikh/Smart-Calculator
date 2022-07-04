import tokenize
from io import StringIO
from collections import deque
import re


class Expression:
	precedence = {"^": 4,
	              "/": 3,
	              "*": 3,
	              "+": 2,
	              "-": 2,
	              "(": 1}

	def __init__(self, exp_str):
		self.exp_str = exp_str
		self.infix_tokens = []
		self.postfix_tokens = []

	def Evaluate(self):
		self.Tokenize()
		self.InfixToPostfix()
		self.EvaluatePostfix()

	def Tokenize(self):
		tuplelist = tokenize.generate_tokens(StringIO(self.exp_str).readline)
		for x in tuplelist:
			if x.string:
				self.infix_tokens.append(x.string)

	def InfixToPostfix(self):
		stack = deque()
		stack.appendleft("(")
		self.infix_tokens.append(")")
		while self.infix_tokens:
			token = self.infix_tokens.pop(0)
			if token == "(":
				stack.appendleft(token)
			elif token == ")":
				while stack[0] != "(":
					self.postfix_tokens.append(stack.popleft())
				stack.popleft()
			elif token == "*" or token == "/" or token == "+" \
				or token == "-" or token == "^":
				while (stack and self.precedence[stack[0]] >= self.precedence[token]):
					self.postfix_tokens.append(stack.popleft())
				stack.appendleft(token)
			else:
				self.postfix_tokens.append(token)

	def EvaluatePostfix(self):
		stack_result = deque()
		while self.postfix_tokens:
			token = self.postfix_tokens.pop(0)
			if token.isdigit():
				stack_result.appendleft(float(token))
			else:
				x = float(stack_result.popleft())
				y = float(stack_result.popleft())
				if token == "+":
					stack_result.appendleft(float(y + x))
				elif token == "-":
					stack_result.appendleft(float(y - x))
				elif token == "*":
					stack_result.appendleft(float(y * x))
				elif token == "/":
					stack_result.appendleft(float(y / x))
				elif token == "^":
					stack_result.appendleft(float(pow(y, x)))

		print(str(round(stack_result.popleft())))


data_dict = {}


while '/exit' != (stroke := input().replace(' ', '')):
	try:
		if stroke == '/help':
			print('The program calculates the sum of numbers')
		elif stroke == '':
			pass
		elif stroke[0] == '/':
			print('Unknown command')
		elif stroke.isalpha():
			if stroke in data_dict:
				print(data_dict[stroke])
			else:
				print('Unknown variable')
		elif '=' in stroke:
			variable, numbers = stroke.split('=')
			if re.fullmatch('[a-zA-Z]+', variable):
				if numbers.isalpha() and numbers in data_dict:
					data_dict[variable] = data_dict[numbers]
				if numbers.isdigit():
					data_dict[variable] = numbers
				elif (re.fullmatch('[a-zA-Z]+', numbers)) and (numbers not in data_dict):
					print('Unknown variable')
				elif not numbers.isalpha():
					print('Invalid assignment')
			else:
				print('Invalid identifier')
		elif stroke[0] == '-':
			print(int(stroke))
		elif ('+' in stroke) or ('-' in stroke) or ('/' in stroke) or ('*' in stroke) \
			or ('^' in stroke) or ('(' in stroke) or (')' in stroke):
			stroke = stroke.replace(' ', '')
			stroke = re.sub(r'[+]+', '+', stroke.replace('--', '+'))
			new_elem = [data_dict[sym] if sym in data_dict else sym for sym in stroke]
			strokes = ''.join(new_elem)
			e = Expression(strokes)
			e.Evaluate()
		else:
			if stroke[0] == '/':
				print('Unknown variable')
			else:
				print('Invalid expression')
	except Exception as err:
		print('Invalid expression')

print('Bye!')


