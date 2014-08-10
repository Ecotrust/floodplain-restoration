

def make_closure(prob):
	print(prob)

	def f_test(a, b):
		return prob[(a,b)]

	return f_test

prob = {('a','b'): 123, ('c','d'): 345}

f = make_closure(prob)
print(f('a', 'b'))
prob[('a', 'b')] = 999

print(f('a', 'b'))

